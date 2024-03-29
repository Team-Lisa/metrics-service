from api.services.users import UserService
import datetime


class UserFrequency:
    USERS_SERVICE = UserService()

    @staticmethod
    def get(from_date, to_date):
        users = UserFrequency.USERS_SERVICE.get_all_users()

        last_connections = [user.get("last_connection") for user in users]
        last_connections = UserFrequency.filter_dates(from_date, to_date, last_connections)
        diff_times = UserFrequency.get_diffs(to_date, last_connections)

        if len(diff_times) == 0:
            return -1

        return UserFrequency.avg_days(diff_times)

    @staticmethod
    def diff_time(date_str_1, date_str_2):
        date_1 = UserFrequency.parse_date(date_str_1)
        date_2 = datetime.datetime.now()
        if date_str_2 != "":
            date_2 = UserFrequency.get_date(date_str_2)

        return (date_2 - date_1).total_seconds()

    @staticmethod
    def parse_date(last_connection):
        last_connection_str = "/".join(last_connection.split("-"))
        return UserFrequency.get_date(last_connection_str)

    @staticmethod
    def get_date(date_str):
        return datetime.datetime.strptime(date_str, "%Y/%m/%d")

    @staticmethod
    def parse(from_date, to_date):
        return {
            "time": UserFrequency.get(from_date, to_date)
        }

    @staticmethod
    def filter_dates(from_date, to_date, last_connections):
        if from_date == "" and to_date == "":
            return last_connections
        elif from_date == "":
            return list(filter(
                lambda last_connection: UserFrequency.parse_date(
                    last_connection) <= UserFrequency.get_date(to_date), last_connections))
        elif to_date == "":
            return list(filter(
                lambda last_connection: UserFrequency.get_date(from_date) <= UserFrequency.parse_date(
                    last_connection), last_connections))
        else:
            return list(filter(
                lambda last_connection: UserFrequency.get_date(from_date) <= UserFrequency.parse_date(
                    last_connection) <= UserFrequency.get_date(to_date), last_connections))

    @staticmethod
    def get_diffs(to_date, last_connections):
        return [UserFrequency.diff_time(date_1, to_date) for date_1 in last_connections]

    @staticmethod
    def avg_days(diff_times):

        total = sum(diff_times)
        total_days = total / (60 * 60 * 24.0)
        return total_days / len(diff_times)