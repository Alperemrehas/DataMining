import csv
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori

itemset_list = []

with open('groceries.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    for row in csv_reader:
        itemset_list.append(row)
        line_count += 1
    print("Total Line Count is : ", line_count)


# Checking the List and Items

def ItemListChecker(list_to_print):
    print("***************" + "ItemLÄ°st Checker Starts" + "***************")
    for i in range(len(list_to_print)):
        print(list_to_print[i])
    print("***************" + "ItemLÄ°st Checker Ends" + "***************")


# Creating Frequent Itemset
def TransEncode(list_to_process):
    te = TransactionEncoder()
    te_data = te.fit(list_to_process).transform(list_to_process)
    df = pd.DataFrame(te_data, columns=te.columns_)
    print("***************" + "TrensactionEncoder Starts" + "***************")
    # print(df)
    print("***************" + "TrensactionEncoder Ends" + "***************")
    return df


# Starting Apriroi Standart
base_df = TransEncode(itemset_list)
freq_items = apriori(base_df, min_support=0.02, use_colnames=True, verbose=1)
print("*******************Base_Df Transaction Ends***********************\n")

# Starting Partition groceries.csv data set into i partitions
def chunker(rowsize):
    input_csv = 'groceries.csv'
    f_ind = 1;
    for i in range(1, line_count, rowsize):
        df = pd.read_csv(input_csv, header=None, nrows=rowsize, skiprows=i)
        output_csv = "chunk" + str(f_ind) + '.csv'
        df.to_csv(output_csv,
                  index=False,
                  header=False,
                  mode='w+',
                  chunksize=rowsize)
        f_ind = f_ind + 1
    print("Chunks Creation Completed...")

# Checking the Frequent Items
print("***********Frequent Items List Start in Apriori**************\n")
print(freq_items)
size_freq_items = len(freq_items) - 1
print("***********Frequent Items List Ends in Apriori**************\n")
for i in range (5,10):
    rowsize = int(line_count / i)
    chunker(rowsize)
print("Row size for each chunks : ", rowsize)

# Reading from Every Chunks .csv file to chunklists
def ChunktoList(chunkname):
    chunkList = []
    with open(chunkname) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            chunkList.append(row)
            line_count += 1
    return chunkList

# Creating chunkList to be used in Apriori next
chunk_1_List = ChunktoList('chunk1.csv')
chunk_2_List = ChunktoList('chunk2.csv')
chunk_3_List = ChunktoList('chunk3.csv')
chunk_4_List = ChunktoList('chunk4.csv')
chunk_5_List = ChunktoList('chunk5.csv')

# ItemListChecker(chunk_1_List)
chunk1_df = TransEncode(chunk_1_List)
chunk1_freq_items = apriori(chunk1_df, min_support=0.02, use_colnames=True, verbose=1)
chunk2_df = TransEncode(chunk_2_List)
chunk2_freq_items = apriori(chunk2_df, min_support=0.02, use_colnames=True, verbose=1)
chunk3_df = TransEncode(chunk_3_List)
chunk3_freq_items = apriori(chunk3_df, min_support=0.02, use_colnames=True, verbose=1)
chunk4_df = TransEncode(chunk_4_List)
chunk4_freq_items = apriori(chunk4_df, min_support=0.02, use_colnames=True, verbose=1)
chunk5_df = TransEncode(chunk_5_List)
chunk5_freq_items = apriori(chunk5_df, min_support=0.02, use_colnames=True, verbose=1)
# print("***********Frequent Items chunk1_freq_items Start in Apriori**************\n")
# print(chunk1_freq_items)
size_chunk1 = len(chunk1_freq_items) - 1
size_chunk2 = len(chunk2_freq_items) - 1
size_chunk3 = len(chunk3_freq_items) - 1
size_chunk4 = len(chunk4_freq_items) - 1
size_chunk5 = len(chunk5_freq_items) - 1

print("size of frequent itemset of chunk1 : ", size_chunk1)
print("size of frequent itemset of chunk2 : ", size_chunk2)
print("size of frequent itemset of chunk3 : ", size_chunk3)
print("size of frequent itemset of chunk4 : ", size_chunk4)
print("size of frequent itemset of chunk5 : ", size_chunk5)
# print("***********Frequent Items chunk1_freq_items Ends in Apriori**************\n")

SON_List = []
SON_List = list(
    set().union(chunk1_freq_items, chunk2_freq_items, chunk3_freq_items, chunk4_freq_items, chunk5_freq_items))
size_SON_list = len(SON_List)
print("size of frequent itemset of SON List : ", size_SON_list)
over_generation_ration = size_SON_list / size_freq_items
print("Over Generation Ration is :", over_generation_ration)
