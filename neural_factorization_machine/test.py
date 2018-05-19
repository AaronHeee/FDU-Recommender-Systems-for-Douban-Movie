import LoadData as DATA

path = 'data/'
dataset = 'frappe'
loss_type = 'square_loss'

data = DATA.LoadData(path, dataset, loss_type)
print(data.Train_data)
