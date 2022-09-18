from prometheus_pandas import query
from datetime import datetime


class EnergyReport:
    def __init__(self):
        print("Initialize Energy Report...")
        self.electric = 15.5  # number of cents per kWh
        self.prom_port = 9090
        self.server_addr = '192.168.1.3'
        self.report_path = '/home/bunchies/gits/energyReport/reports'
        self.metric = 'tasmota_energy_power_active_watts'
        self.start_date = '2022-09-01T00:00:00Z'
        self.end_date = '2022-09-30T23:59:59Z'
        self.increment = '1d'
        print("Begin Report Generation")
        # self.generateReport()
        print("Report Generation Complete.")

    def powerConversion(self, wattage):
        # converts a given wattage to daily cost
        kwh = wattage * 24 / 1000  # 24 hrs
        cents = 100
        return kwh * self.electric / cents

    def generateReport(self):
        print("Querying Prometheus for Electricity Utilization...")
        p = query.Prometheus(f'http://{self.server_addr}:{self.prom_port}')
        results = p.query_range(self.metric,
                                self.start_date,
                                self.end_date,
                                self.increment)
        sums = results.sum(axis=1)
        # print(results)
        results['Watts'] = sums
        results['Total KW Hours'] = sums * 24 / 1000
        results['Cost $USD'] = round(self.powerConversion(sums), 2)
        # filename = f'energy_report-{datetime.now().strftime("%m-%d-%YT%H:%M:%S")}.csv'
        filename = f'energy_report-{self.start_date.split("T")[0]}-to-{self.end_date.split("T")[0]}.csv'
        print(f"saving to {filename}")
        results.to_csv(f"{self.report_path}/{filename}")


report = EnergyReport()
report.generateReport()
"""

#!/usr/bin/python

from prometheus_pandas import query
from datetime import datetime

electric = 15.5 # number of cents per kWh

p = query.Prometheus('http://192.168.1.3:9090')
results = p.query_range(
        'tasmota_energy_power_active_watts',
        '2022-09-01T00:00:00Z', '2022-09-30T23:59:59Z', '1d')
print(results)
sums = results.sum(axis=1)
def powerConversion(wattage):
        # converts a given wattage to daily cost
        kwh = wattage * 24 / 1000  # 24 hrs
        cents = 100
        return kwh * electric / cents

results['Watts'] = sums
results['Total KW Hours'] = sums * 24 / 1000
results['Cost $USD'] = round(powerConversion(sums), 2)
filename=f'/home/bunchies/gits/energyReport/energy_report-{datetime.now().strftime("%m-%d-%YT%H:%M:%S")}.csv'
print(f"saving to {filename}")
results.to_csv(filename)"""