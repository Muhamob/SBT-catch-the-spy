import json


def fill_meta_data(user):
    if type(user["cards"]["card"]) is list:
        for card in user["cards"]["card"]:
            if type(card["activities"]["activity"]) is list:
                meta_data = list()
                for activity in card["activities"]["activity"]:
                    activity_dict = dict()
                    activity_dict["Date"] = activity["Date"]
                    activity_dict["Departure"] = activity["Departure"]
                    activity_dict["Arrival"] = activity["Arrival"]
                    meta_data.append(activity_dict)
            else:
                meta_data = dict()
                activity = card["activities"]["activity"]
                meta_data["Date"] = activity["Date"]
                meta_data["Departure"] = activity["Departure"]
                meta_data["Arrival"] = activity["Arrival"]

    else:
        card = user["cards"]["card"]
        if type(card["activities"]["activity"]) is list:
            meta_data = list()
            for activity in card["activities"]["activity"]:
                activity_dict = dict()
                activity_dict["Date"] = activity["Date"]
                activity_dict["Departure"] = activity["Departure"]
                activity_dict["Arrival"] = activity["Arrival"]
                meta_data.append(activity_dict)
        else:
            meta_data = dict()
            activity = card["activities"]["activity"]
            meta_data["Date"] = activity["Date"]
            meta_data["Departure"] = activity["Departure"]
            meta_data["Arrival"] = activity["Arrival"]
    return meta_data


def main():
    with open("output.json", "r") as f:
        data = json.load(f)

    extracted_data = list()

    for user in data:
        user_dict = dict()
        user_dict["name"] = user['name']['@first']
        user_dict["surname"] = user['name']['@last']
        meta_data = fill_meta_data(user)
        user_dict["meta"] = meta_data
        extracted_data.append(user_dict)

        f = open("extracted_data_with_meta.json", 'w')
        json.dump(extracted_data, f, indent=4)
        f.close()

if __name__ == main():
    main()