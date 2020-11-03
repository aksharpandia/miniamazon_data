import pandas as pd
import warnings
import json
warnings.simplefilter(action='ignore', category=FutureWarning)
import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' ) 

#there is some weird stuff at 2004th row of csv, I got rid of that when doing this. so the CSV I have is not an exact replica of Kaggle


#getting all the data from ratings col in csv, putting in a list. putting None for empty cells

def clean_data(csv):
    data = pd.read_csv(csv)
    count = 0;
    for line in range(2000): # could use len(data) here, but requirements only say >=1000 values
        raw_sellers = data.iloc[line]['sellers']
        if raw_sellers == raw_sellers: # will only work with rows that have sellers
            count += 1
            process_seller_row(data, line)
            # add more helper functions to process other values per row (ie, product, review, etc.)
        else:
            continue
    print(count)

def process_seller_row(data, line):
    # print('---- new product ----')
    string_json_sellers = data.iloc[line]['sellers'].replace('=>', ':')
    json_sellers = json.loads(string_json_sellers)
    has_multiple_sellers = isinstance(json_sellers['seller'], list)
    sellers = json_sellers['seller']
    if has_multiple_sellers:
        for seller in sellers:
            process_single_seller(seller)
    else:
        process_single_seller(sellers)

def process_single_seller(seller):
    # print('---- new seller ----')
    seller_price = 0.00
    seller_name = ''
    for attr, value in seller.items():
        if ('Seller_name' in attr):
            seller_name = value
        if ('Seller_price' in attr):
            seller_price = value
    # print(seller_name)
    # print(seller_price)

def get_all_ratings(csv):
    data = pd.read_csv(csv) #reads in the csv
    all_ratings = []
    count = 0
    for i in range(len((data['average_review_rating']))):
        raw_rating = data.iloc[i]['average_review_rating']
        if raw_rating == raw_rating: #checking for NaN, any NaNs are not equal to self
            rating = float(raw_rating[0:3]) 
            all_ratings.append(rating)
        else:
            all_ratings.append(None)
            count+=1
    return all_ratings

#getting all the data from number of reviews col in csv, putting in a list. putting None for empty cells

def get_all_numberofreviews(csv):
    data = pd.read_csv(csv)
    all_numberofreviews = []
    count = 0
    for i in range(len((data['number_of_reviews']))):
        count += 1
        raw_number_of_reviews = data.iloc[i]['number_of_reviews']
        if raw_number_of_reviews == raw_number_of_reviews:
            number_of_reviews = locale.atoi(raw_number_of_reviews) #getting rid of commas in numbers
            all_numberofreviews.append(int(number_of_reviews))
        else:
            all_numberofreviews.append(None)
    return all_numberofreviews

def get_all_reviewinfo(csv):
    data = pd.read_csv(csv)
    all_review_info = {}
    count = 0
    for i in range(len((data['customer_reviews']))):
        count += 1
        raw_review_info = data.iloc[i]['customer_reviews']
        if raw_review_info == raw_review_info:
            review_info = raw_review_info.strip().split("//")
            commentary = review_info[4]
            date = review_info[2].strip()#getting date
            misc = review_info[3].split()
            for idx in range(len(misc)):#finding where in the string the name is, it's right before on
                if misc[idx]=='on':
                    on = idx
            reviewer_name = ' '.join(misc[1:on])
            all_review_info[i]=[reviewer_name, commentary, date]
        else:
            all_review_info[i]=None #keys of dictioniaries are just the row number
    return all_review_info

# all_ratings = print(len(get_all_ratings('amazon_co-ecommerce_sample.csv')))
# all_numberofreviews = print(len(get_all_numberofreviews('amazon_co-ecommerce_sample.csv')))
# get_all_reviewinfo = print(len(get_all_reviewinfo('amazon_co-ecommerce_sample.csv')))
clean_data('amazon_co-ecommerce_sample.csv')




