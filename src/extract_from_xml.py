import json


def main():
    with open("output.json", "r") as f:
        data = json.load(f)

    extracted_data = list()

    for user in data:
        user_dict = dict()
        user_dict["name"] = user['name']['@first']
        user_dict["surname"] = user['name']['@last']
        extracted_data.append(user_dict)

        f = open("extracted_data.json", 'w')
        json.dump(extracted_data, f, indent=4)
        f.close()

if __name__ == main():
    main()