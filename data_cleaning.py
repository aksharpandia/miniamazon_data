import pandas as pd
import warnings
import json
import unicodedata2
warnings.simplefilter(action='ignore', category=FutureWarning)
import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' ) 

#there is some weird stuff at 2004th row of csv, I got rid of that when doing this. so the CSV I have is not an exact replica of Kaggle


#getting all the data from ratings col in csv, putting in a list. putting None for empty cells

def clean_data(csv):
    data = pd.read_csv(csv)
    count = 0;
    for line in range(1): # could use len(data) here, but requirements only say >=1000 values
        raw_sellers = data.iloc[line]['sellers']
        if raw_sellers == raw_sellers: # will only work with rows that have sellers
            count += 1
            process_seller_row(data, line)
            # add more helper functions to process other values per row (ie, product, review, etc.)
        else:
            continue
    print(count)

# global var?
all_product_info = []

def process_single_product(seller, data, line):
    # modelNum ('uniq_id'), userID ('seller_name_x'), productDescription ('product_description' + 'product_info'), 
    # productName ('product_name'), productImage (PLACEHOLDER for now)
    # stockLeft ('number_available_in_stock'), isRecommended (yes if 'average_review_rating' is >= 4.0)
    product_count = 0
    seller_price = 0.00
    seller_name = ''
    single_product_info = []
    for attr, value in seller.items():
        if ('Seller_name' in attr):
            seller_name = value
        if ('Seller_price' in attr):
            seller_price = value

    model_number = data.iloc[line]['uniq_id'].strip()
    raw_description = str(data.iloc[line]['product_description'])
    raw_info = str(data.iloc[line]['product_information'])
    product_des = (raw_description + '\n \n' + raw_info)
    # product_description.replace('\xa0', u'\n')
    product_description = unicodedata2.normalize("NFKD", product_des)
    product_name = data.iloc[line]['product_name'].strip()
    product_image = 'img1.jpg'
    stock = data.iloc[line]['number_available_in_stock'].split('\xa0new')
    stock_left = stock[0]
    raw_rating = data.iloc[line]['average_review_rating']
    rating = 0.0
    if raw_rating == raw_rating: #checking for NaN, any NaNs are not equal to self
        rating = float(raw_rating[0:3]) 
    if (rating >= 4.0):
        is_recommended = True
    else:
        is_recommended = False 
    product_count+=1
    single_product_info.extend([model_number, seller_name, product_description, product_name, product_image,
    stock_left, is_recommended, seller_price])
    
    print(single_product_info)
    all_product_info.append(single_product_info)
    return single_product_info

def process_seller_row(data, line):
    # print('---- new product ----')
    string_json_sellers = data.iloc[line]['sellers'].replace('=>', ':')
    json_sellers = json.loads(string_json_sellers)
    has_multiple_sellers = isinstance(json_sellers['seller'], list)
    sellers = json_sellers['seller']
    if has_multiple_sellers:
        for seller in sellers:
            process_single_seller(seller)
            process_single_product(seller, data, line)
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
        modelNum = data.iloc[i]['uniq_id']
        if raw_review_info == raw_review_info:
            separate_reviews = raw_review_info.strip().split("|") #finding each separate review for each product, then decomposing each specific review
            for rev in separate_reviews:
                review_info = rev.split(" // ")
                if len(review_info) > 2: #some reviews for a product are incomplete, so we will skip them. for example, product in row 1704 has an
                    headline = review_info[0].strip()
                    #checking if commentary exists; if it doesn't just inserting nothing for commentary
                    try:
                        commentary = review_info[4].strip()
                    except IndexError:
                        commentary = ""
                    date = review_info[2].strip()#getting date
                    misc = review_info[3].split()
                    user_rating = float(review_info[1].strip())

                    for idx in range(len(misc)):#finding where in the string the name is, it's right before on
                        if misc[idx]=='on':
                            on = idx
                    reviewer_name = ' '.join(misc[1:on])

                    if i not in all_review_info: #if a dict entry does not already exist for a product
                        all_review_info[modelNum]=[[user_rating, headline, commentary, date, reviewer_name, modelNum]]
                    else:
                        all_review_info[modelNum].append([user_rating, headline, commentary, date, reviewer_name, modelNum])
        else:
            all_review_info[modelNum]=None #keys of dictioniaries are just the row number
    return all_review_info

# all_ratings = print(len(get_all_ratings('amazon_co-ecommerce_sample.csv')))
# all_numberofreviews = print(len(get_all_numberofreviews('amazon_co-ecommerce_sample.csv')))
# get_all_reviewinfo = print(len(get_all_reviewinfo('amazon_co-ecommerce_sample.csv')))
clean_data('amazon_co-ecommerce_sample.csv')