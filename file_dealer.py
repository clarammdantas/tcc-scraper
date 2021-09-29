import glob
import csv

# 1. merge files by group (payments or details)
def merge_details():
    details_path = glob.glob('./transrobot/details*.csv')
    assert(len(details_path) == 154)

    file_counter = 0
    with open('./transrobot/details_merged.csv', 'a') as new_file:
        for path in details_path:
            with open(path, 'r') as detail_file:
                if file_counter > 0:
                    detail_file.__next__()

                for line in detail_file:
                    new_file.write(line)

            file_counter += 1

# print(len(open('./transrobot/details_merged.csv').readlines()))

def merge_payments():
    payments_path = glob.glob('./transrobot/payments*.csv')
    assert(len(payments_path) == 7)

    file_counter = 0
    with open('./transrobot/payments_merged.csv', 'a') as new_file:
        for path in payments_path:
            with open(path, 'r') as payments_file:
                if file_counter > 0:
                    payments_file.__next__()

                for line in payments_file:
                    new_file.write(line)

            file_counter += 1

# 3. merge two files (payments and details)
def merge_details_and_payments():
    current_line = 1
    with open('./transrobot/payments_details2.csv', 'a') as new_file:
        line_header = 0
        new_file_writer = csv.writer(new_file,
                                     delimiter=',',
                                     quotechar='"',
                                     quoting=csv.QUOTE_MINIMAL)

        with open('./transrobot/payments_merged.csv', 'r') as payment_file:
            payment_file_csv = csv.reader(payment_file, delimiter=',', quotechar='"')
            for line in payment_file_csv:
                print(current_line)
                current_line += 1

                with open('./transrobot/details_merged.csv', 'r') as details_file:
                    details_csv = csv.reader(details_file, delimiter=',', quotechar='"')
                    if line_header == 0:
                        details_header = details_csv.__next__()
                        new_file_writer.writerow(line + details_header)
                        line_header += 1

                    else:
                        # payment_values = line.rstrip().split(',')

                        # 1 = empenho, 2 = favorecido
                        empenho = line[1].split('NE')[-1]
                        # Remove trailling 0
                        payment_id = str(int(empenho)) + line[2]
                        value = ['NA' for i in range(22)]
                        # value = ','.join(value)
                        # value += '\n'
                        details_line = 1

                        for line_detail in details_csv:
                            if details_line == 1:
                                details_line += 1
                                continue

                            detail_id = str(int(line_detail[14])) + line_detail[13]
                            if payment_id == detail_id:
                                    value = line_detail
                                    break


                        new_file_writer.writerow(line + value)

merge_details_and_payments()
