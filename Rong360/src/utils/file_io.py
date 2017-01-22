import csv

def csv_write_file(filename, data_list):
    csvfile = file(filename, 'wb')

    #print str(data_list) + " " + str( type(data_list[0]))

    writer = csv.writer(csvfile)
    writer.writerows(data_list)

    #for r in data_list:
    #    writer.writerow(list(r))

    csvfile.close()