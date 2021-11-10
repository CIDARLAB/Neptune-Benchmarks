#! /usr/bin/env python3

import glob
from parchmint import Device
import sys
import json

files = glob.glob("./**/*.json", recursive=True)

for file_path in files:

    print("File Name: " + file_path)

    device = None

    with open(file_path) as data_file:
        text = data_file.read()
        device_json = json.loads(text)
        device = Device(device_json)

    print("Checking for components with no dimensions:")
    for component in device.components:
        if component.xspan < 0 or component.yspan < 0:
            print(
                "ERROR !!! - Component - {} | Type - {} | Dimensions - ({}, {})".format(
                    component.ID, component.entity, component.xspan, component.yspan
                )
            )
        for port in component.ports:
            if port.x < 0 or port.y < 0:
                "ERROR !!! - Component - {} | Type - {} | Port {} - ({}, {})".format(
                    component.ID, component.entity, port.label, port.x, port.y
                )

    print("Checking for components with 0 dimensions:")
    for component in device.components:
        if component.xspan == 0 or component.yspan == 0:
            print(
                "ERROR !!! - Component - {} | Type - {} | Dimensions - ({}, {})".format(
                    component.ID, component.entity, component.xspan, component.yspan
                )
            )

    print("Checking for components with no ports:")
    for component in device.components:
        if len(component.ports) == 0:
            print(
                "ERROR !!! - Component - {} | Type - {}".format(
                    component.ID, component.entity
                )
            )

    # Check if any of the ports are outside of the bounds of the device
    print("Checking for ports outside of device bounds:")
    for component in device.components:
        xmax = component.xspan
        ymax = component.yspan
        for port in component.ports:
            if port.x > xmax or port.y > ymax:
                print(
                    "ERROR !!! - Component - {} | Type - {} | Port {} - ({}, {}) | Dim - ({}, {})".format(
                        component.ID,
                        component.entity,
                        port.label,
                        port.x,
                        port.y,
                        xmax,
                        ymax,
                    )
                )

    # Check for connections with missing ports on targets
    print("Checking for connections with missing ports on targets:")
    for connection in device.connections:
        if connection.source is None:
            print(
                "ERROR !!! - Source set to None on connection: {}".format(connection.ID)
            )
        else:
            target = connection.source
            if target.port is None:
                print(
                    "ERROR !!! - Target port set to None on connection: {} target: {}".format(
                        connection.ID, target.component
                    )
                )
        if len(connection.sinks) == 0:
            print("ERROR !!! - No sinks on connection: {}".format(connection.ID))
        else:
            for sink in connection.sinks:
                if sink.port is None:
                    print(
                        "ERROR !!! - Sink port set to None on connection: {} sink: {}".format(
                            connection.ID, sink.component
                        )
                    )
