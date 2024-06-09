filter_conditions=[]
fields_to_check={
    '3':3,
    '4':4

}
body={
    '1':1,
    '2':2,
    '3':3,
}
fields_to_check['3'].replace(str(body['3']), '333')
print(filter_conditions)