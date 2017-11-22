from netCDF4 import Dataset
import numpy as np
from datetime import timedelta
from datetime import datetime as dt
import matplotlib.pyplot as plt

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


if __name__ == "__main__":

    start = dt(2017,5,1)
    ende = dt.today()

    gen_low_max = 0
    gen_total_max = 0

    low_max_list = []
    total_max_list = []
    low_values = []
    total_values = []

    with open("DustIndexStats.csv", "w") as f:
        f.write("MaxDILow;MaxDITotal")
        for date in daterange(start,ende):
            datestr = date.strftime("%Y%m%d")
            NC_PATH = "/pool/OBS/ACPC/RamanLidar-LICHT/3_QuickLook/nc/ql{}/".format(datestr[2:6])
            NC_NAME = "/li{}.b532".format(datestr[2:])

            # Get data from nc-file:
            try:
                nc = Dataset(NC_PATH + NC_NAME)
            except:
                continue
            dustIndexLow = nc.variables["DustIndexLowLayer"][:].copy()
            dustIndexTotal = nc.variables["DustIndexTotal"][:].copy()
            seconds = nc.variables["Time"][:].copy()
            nc.close()

            # Handle missing Values:
            dustIndexTotal[np.where(dustIndexTotal > 1e30)] = np.nan
            dustIndexLow[np.where(dustIndexLow > 1e30)] = np.nan

            for to,lo in zip(dustIndexTotal,dustIndexLow):
                low_values.append(lo)
                total_values.append(to)

            total_max = np.nanmax(dustIndexTotal)
            low_max = np.nanmax(dustIndexLow)

            total_max_list.append(total_max)
            low_max_list.append(low_max)

            if total_max > gen_total_max:
                print(total_max)
                gen_total_max = total_max

            if low_max > gen_low_max:
                print(low_max)
                gen_low_max = low_max


            f.write("%9.7f"%low_max + ";%9.7f"%total_max + "\n")


    low_max_list = [x for x in low_max_list if not np.isnan(x)]
    total_max_list = [x for x in total_max_list if not np.isnan(x)]
    low_values = [x for x in low_values if not np.isnan(x)]
    total_values = [x for x in total_values if not np.isnan(x)]


    print("Total Maximum for Dust Index Low: %9.7f"%gen_low_max)
    print("Total Maximum for Dust Index Total: %9.7f"%gen_total_max)

    fig,((ax1,ax2),(ax3,ax4),(ax5,ax6)) = plt.subplots(nrows=3,ncols=2,figsize=(16,9))


    ax1.set_title("Dust Index low, maximum distribution")
    ax2.set_title("Dust Index total, maximum distribution")
    ax3.set_title("Dust Index Low")
    ax4.set_title("Dust Index Total")

    nbins = 20
    ax1.hist(low_max_list,bins=nbins)
    ax2.hist(total_max_list,bins=nbins)
    ax3.hist(low_values,bins=nbins)
    ax4.hist(total_values,bins=nbins)
    plt.tight_layout()

    low_values = np.asarray(low_values)
    total_values = np.asarray(total_values)

    ax6.boxplot(total_values,1,"+")
    ax5.boxplot(low_values,5,"+")
    plt.savefig("DI_stats.png")


