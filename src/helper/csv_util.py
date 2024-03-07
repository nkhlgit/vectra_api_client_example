def to_csv(ext, data_list):
    if ext == 'groups': 
        for data in data_list:
            data['members'] =  ','.join(data['members'])
        return data_list
    else:
        return data_list
        