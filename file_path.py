data_path = 'C:/Users/Гриша/PycharmProjects/proxy_bot/data'
#data_path = '/home/proxy_bot/data'


def work_on_new_user(user_id):
    is_new_user = True

    with open(f'{data_path}/users_id.txt', 'r') as file_with_users:
        for line in file_with_users:
            if line == str(user_id) or line[:-1] == str(user_id):
                is_new_user = False
    if is_new_user:
        with open(f'{data_path}/users_id.txt', 'a') as file_with_users:
            file_with_users.write(f'{str(user_id)}\n')
        with open(f'{data_path}/uniq_people_counter.txt', 'r') as file_with_users:
            current_number_of_users = int(file_with_users.readline())
        with open(f'{data_path}/uniq_people_counter.txt', 'w') as file_with_users:
            file_with_users.write(str(current_number_of_users + 1))


def get_users_count():
    with open(f'{data_path}/uniq_people_counter.txt', 'r') as file_with_users:
        return file_with_users.readline()


def parse_count():
    with open(f'{data_path}/proxy_ask_counter.txt', 'r') as file_with_users:
        return file_with_users.readline()


def parse_success():
    with open(f'{data_path}/proxy_ask_counter.txt', 'r') as file_with_users:
        current_number_of_users = int(file_with_users.readline())
    with open(f'{data_path}/proxy_ask_counter.txt', 'w') as file_with_users:
        file_with_users.write(str(current_number_of_users + 5))

