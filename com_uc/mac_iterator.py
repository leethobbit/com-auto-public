import csv
#import com_nornir

with open('com_nornir/backups/phones_trimmed.csv') as f:
    reader = csv.DictReader(f)
    # Creates a list of all MAC addresses from the csv file
    macs = [line['MAC_ADDR'] for line in reader]

with open('com_nornir/backups/phones_trimmed_edited.csv', 'w') as f:
    fields = ['MAC_ADDR','MAC_ADDR2']
    writer = csv.writer(f)
    for macs in macs:
        res = '.'.join(macs[i:i + 4] for i in range(0, len(macs), 4))
        print(res)
        writer.writerow(res)
        #writer.writerow(res)
        #writer.writerows(res)

# Convert the MACs from '0C1167236C0F' format to '0C11.6723.6C0F'

    # print(res)

