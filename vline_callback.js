var geometry = cb_data['geometry'];
var data = line_source.data;
var source_data = source.data["time"];
var x0 = geometry['x'];

if (x0 < 1e20) {
    document.getElementById("buttonInfo").innerHTML = x0;
} else {
    x0=source_data[0];
}
data['x'] = [x0];
line_source.change.emit();

