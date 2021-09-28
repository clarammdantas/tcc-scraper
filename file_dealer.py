import glob

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
    with open('./transrobot/payments_details.csv', 'a') as new_file:
        line_header = 0
        with open('./transrobot/payments_merged.csv', 'r') as payment_file:
            for line in payment_file:
                print(current_line)
                current_line += 1
                with open('./transrobot/details_merged.csv', 'r') as details_file:
                    if line_header == 0:
                        details_header = details_file.__next__()
                        new_header = line.rstrip() + ',' + details_header
                        new_file.write(new_header)
                        line_header += 1

                    else:
                        payment_values = line.rstrip().split(',')

                        # 1 = empenho, 2 = favorecido
                        id = payment_values[1] + payment_values[2]
                        value = ['NA' for i in range(22)]
                        value = ','.join(value)
                        value += '\n'

                        for line_detail in details_file:
                            details_values = line_detail.split(',')

                            # nome_razao_social = 13, id_empenho = 9
                            detail_id = details_values[9] + details_values[13]
                            if id == detail_id:
                                value = line_detail
                                break

                        new_file.write(line.rstrip() + ',' + value)

merge_details_and_payments()
