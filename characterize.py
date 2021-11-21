from parchmint import Device
import numpy as np
import sys
import json
import glob
from tabulate import tabulate


# file_path = sys.argv[1]

# print("File Name: " + file_path)


device = None


files = glob.glob("./**/*.json", recursive=True)
# Create 2d numpy array for storing the file info
file_info = np.empty((len(files), 11), dtype=object)

index = 0
for file_path in files:
    with open(file_path) as data_file:
        text = data_file.read()
        device_json = json.loads(text)
        device = Device(device_json)

        # Save device name
        file_info[index, 0] = device.name

        # Save number of components in the device
        file_info[index, 1] = len(device.components)
        # Save number of connections in the device
        file_info[index, 2] = len(device.connections)

        # Save number of valves in the device
        file_info[index, 3] = len(device.valves)

        # Save the number of layers in the device
        file_info[index, 4] = len(device.layers)

        # Save yes if the device has a layer of type CONTROL
        file_info[index, 5] = (
            "YES" if "CONTROL" in [layer.type for layer in device.layers] else "NO"
        )

        # Save the max connectiveity of the connection in the device
        file_info[index, 6] = max(
            [len(connection.sinks) + 1 for connection in device.connections]
        )

        # Save the standard deviation of the component areas in the device
        file_info[index, 7] = (
            np.std(
                [component.xspan * component.yspan for component in device.components]
            )
            / 10e6
        )

        # Save the mean of the component areas in the device
        file_info[index, 8] = (
            np.mean(
                [component.xspan * component.yspan for component in device.components]
            )
            / 10e6
        )

        # Save the xspan and yspan of the component with the largest area in the device
        file_info[index, 9] = (
            device.components[
                np.argmax(
                    [
                        component.xspan * component.yspan
                        for component in device.components
                    ]
                )
            ].xspan
            / 1000,
            device.components[
                np.argmax(
                    [
                        component.xspan * component.yspan
                        for component in device.components
                    ]
                )
            ].yspan
            / 1000,
        )

        # Save the xspan and yspan of the component with the smallest area in the device
        file_info[index, 10] = (
            device.components[
                np.argmin(
                    [
                        component.xspan * component.yspan
                        for component in device.components
                    ]
                )
            ].xspan
            / 1000,
            device.components[
                np.argmin(
                    [
                        component.xspan * component.yspan
                        for component in device.components
                    ]
                )
            ].yspan
            / 1000,
        )

    index += 1


# Save the numpy array to a tsv file with the corresponding headers
np.savetxt(
    "characterize.tsv",
    file_info,
    delimiter="\t",
    fmt="%s",
    header="Name\tComponents\tConnections\tValves\tLayers\tControl\tMaxConnectivity\tStdDevArea\tMeanArea\tMax(Xspan,Yspan)\tMin(Xspan,Yspan)",
)

# Generate Header list to be used in tabulate
headers = [
    "Name",
    "Components",
    "Connections",
    "Valves",
    "Layers",
    "Control",
    "MaxConnectivity",
    "StdDevArea",
    "MeanArea",
    "Max(Xspan,Yspan)",
    "Min(Xspan,Yspan)",
]

print(tabulate(file_info, headers=headers, tablefmt="latex", floatfmt=".2f"))
