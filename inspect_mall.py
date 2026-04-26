import scipy.io
import numpy as np

mall_gt = scipy.io.loadmat('mall_dataset/mall_gt.mat')
print('Keys:', [k for k in mall_gt.keys() if not k.startswith('__')])
frame_data = mall_gt['frame']
print('frame shape:', frame_data.shape)
print('frame dtype:', frame_data.dtype)
print('frame dtype names:', frame_data.dtype.names)
print('First frame loc shape:', frame_data[0]['loc'].shape)
print('First frame loc:', frame_data[0]['loc'][:5])
print('Type of loc:', type(frame_data[0]['loc']))
print('Dtype of loc:', frame_data[0]['loc'].dtype)