"""
The CPUCollector collects CPU utilization metric using ... /proc/stat

#### Dependencies
  * /proc/stat

"""

import os
import time

try: 
    import psutil
except ImportError:
    psutil = None

class CPUCollector():
    PROC = '/proc/stat'
    INTERVAL = 1
    SIMPLE = False

    def __init__(self):
        self.last_values = {}

    def derivative(self, path, new, max_valie=0):
        """
        Calculate the derivative of metric
        """
        if path in self.last_values:
            old = self.last_values[path]

            if new < old:
        old 

        

    def collect(self):
        """
        get cpu time list
        """

        def cpu_time_list():
            """
            get cpu time list
            """
            statFile = open(self.PROC, 'r')
            timeList = statFile.readline().split(" ")[2:6]
            for i in range(len(timeList)):
                timeList[i] = int(timeList[i])
            statFile.close()
            return timeList

        def cpu_delta_time(interval):
            """
            get before and after cpu times for usage calc
            """
            pre_check = cpu_time_list()
            time.sleep(interval)
            post_check = cpu_time_list()

            for i in range(len(pre_check)):
                post_check[i] -= pre_check[i]

            return post_check

        if os.access(self.PROC, os.R_OK):
            
            # If SIMPLE ... only return aggregate CPU% metric
            if self.SIMPLE:
                dt = cpu_delta_time(self.INTERVAL)
                cpuPct = 100 - (dt[len(dt)-1]*100.00 / sum(dt))
                
                # self.publish('percent', str('%.4f' % cpuPct))
                print('percent {%.4f}' % cpuPct)

                return True 

            results = {}

            # Open file
            file = open(self.PROC, 'r')

            ncpus = -1  # do not want to count the ..cpu(total)
            for line in file:
                if not line.startswith('cpu'):
                    continue

                ncpus += 1
                elements = line.split()
                
                cpu = elements[0]

                if cpu == 'cpu':
                    cpu = 'total'
                
                results[cpu] = {}

                if len(elements) >= 2:
                    results[cpu]['user'] = elements[1]
                if len(elements) >= 3:
                    results[cpu]['nice'] = elements[2]
                if len(elements) >= 4:
                    results[cpu]['system'] = elements[3]
                if len(elements) >= 5:
                    results[cpu]['idle'] = elements[4]
                if len(elements) >= 6:
                    results[cpu]['iowait'] = elements[5]
                if len(elements) >= 7:
                    results[cpu]['irq'] = elements[6]
                if len(elements) >= 8:
                    results[cpu]['softirq'] = elements[7]
                if len(elements) >= 9:
                    results[cpu]['steal'] = elements[8] 
                if len(elements) >= 10:
                    results[cpu]['guest'] = elements[9]
                if len(elements) >= 11:
                    results[cpu]['guest_nice'] = elements[10]  

            # Close file
            file.close()

            metrics = {'cpu_count', ncpus}
            
            for cpu in results.keys():
                stats = results[cpu]
                for s in stats.keys():
                    metric_name = '.'.join([cpu,s])
                    
                    #Get actual data
                    if ()


            return results