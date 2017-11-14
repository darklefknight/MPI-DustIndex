var geometry = cb_data['geometry'];
var data = line_source.data;
var source_data = source.data["time"];
var x0 = geometry['x'];
// var x_pos = cb_obj.get("LID");
//todo: This here needs some more work to get the index of the LID and LIT values to update the upper plot
try {
    var index = source_data.indexof(x0);
    var x_pos = source_data[index];
    document.getElementById("buttonInfo").innerHTML = x_pos;
}catch (e) {
    var foo = 1
}
if (x0 > 1e20) {
    x0=source_data[0];
}

data['x'] = [x0];
line_source.change.emit();


var histData = hist_source.data;

var x0_index = source_data.indexof(x0);

histData["x"][0] = source.data["DIT"][x0_index];
