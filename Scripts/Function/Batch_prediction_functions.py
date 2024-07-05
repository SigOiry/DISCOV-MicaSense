from osgeo import gdal

from fastbook import *
from pandas.api.types import is_string_dtype, is_numeric_dtype, is_categorical_dtype
from fastai.tabular.all import *
pd.options.display.max_rows = 20
pd.options.display.max_columns = 8
import numpy as np
from matplotlib import colors
import rasterio as rio
import rasterio.mask
import fiona
import matplotlib.pyplot as plt
import warnings
import pandas as d
import gc
import os
import copy

warnings.filterwarnings("ignore")


def batch_prediction(imgs, models):

    for img_i in imgs:

        models_i = copy.copy(models)

        print("----- Prediction on " + img_i)

        for i in range(0,len(models_i)):
            if(os.path.isfile("../Output/Pred/Batch/" + models_i[i] + '/' + img_i + '_' + models_i[i] +"_prob.tif")):
                print('A prediction already exist of the model ' + models_i[i] + ' on ' + img_i)
                models_i[i] = None
        
        models_i = list(filter(lambda item: item is not None, models_i))    
        if len(models_i) != 0:

            print("*-*-*-* Starting preprocessing on the image")

            with fiona.open('../Data/shp/mask/' + img_i + '.shp', "r") as shapefile:
                shapes = [feature["geometry"] for feature in shapefile]
                
            with rio.open('../Data/img/' + img_i + '.tif') as ds:
                arr, out_transform = rasterio.mask.mask(ds, shapes, crop=True)
                out_meta = ds.meta

            gt = [out_transform[2],out_transform[0],out_transform[1],
            out_transform[5],out_transform[3],out_transform[4]]


            lowtif = gdal.Open('../Data/img/' + img_i + '.tif')
            proj = lowtif.GetProjection()
            del lowtif 

            Arr_Max=np.max(arr,axis=0)
            Arr_Min=np.min(arr,axis=0)

            arr_std=(arr - Arr_Min)/(Arr_Max - Arr_Min)

            df_NAN = pd.DataFrame()
            df_NAN['Reflectance_444'] = arr[0].ravel()
            df_NAN['Reflectance_475'] = arr[1].ravel() 
            df_NAN['Reflectance_531'] = arr[2].ravel() 
            df_NAN['Reflectance_560'] = arr[3].ravel() 
            df_NAN['Reflectance_650'] = arr[4].ravel() 
            df_NAN['Reflectance_668'] = arr[5].ravel() 
            df_NAN['Reflectance_705'] = arr[6].ravel() 
            df_NAN['Reflectance_717'] = arr[7].ravel() 
            df_NAN['Reflectance_740'] = arr[8].ravel() 
            df_NAN['Reflectance_842'] = arr[9].ravel()

            df_NAN.replace([0,65535], np.nan, inplace=True)

            df_NAN['Reflectance_Stan_444'] = arr_std[0].ravel()
            df_NAN['Reflectance_Stan_475'] = arr_std[1].ravel() 
            df_NAN['Reflectance_Stan_531'] = arr_std[2].ravel() 
            df_NAN['Reflectance_Stan_560'] = arr_std[3].ravel() 
            df_NAN['Reflectance_Stan_650'] = arr_std[4].ravel() 
            df_NAN['Reflectance_Stan_668'] = arr_std[5].ravel() 
            df_NAN['Reflectance_Stan_705'] = arr_std[6].ravel() 
            df_NAN['Reflectance_Stan_717'] = arr_std[7].ravel() 
            df_NAN['Reflectance_Stan_740'] = arr_std[8].ravel() 
            df_NAN['Reflectance_Stan_842'] = arr_std[9].ravel()

            df_NAN['NDVI'] = (df_NAN['Reflectance_842']-df_NAN['Reflectance_650'])/(df_NAN['Reflectance_842']+df_NAN['Reflectance_650'])
            df_NAN['NDVI_Stan'] = (df_NAN['Reflectance_Stan_842']-df_NAN['Reflectance_Stan_650'])/(df_NAN['Reflectance_Stan_842']+df_NAN['Reflectance_Stan_650'])

            del arr_std, Arr_Max, Arr_Min
            gc.collect()

            df = df_NAN.dropna()


            df_test_nan_nrum = df_NAN
            df_test_nan_nrum['ID'] = np.arange(len(df_test_nan_nrum))
            df_test_nrum = df_test_nan_nrum.dropna()


            del df_test_nan_nrum 

            ID_l=list(df_test_nrum['ID'])

            gc.collect()

            for learn_i in models_i:

                print("****** Predict with " + learn_i)

                learn = load_learner('../models/' + learn_i + '.pkl')
                categories = learn.dls.vocab

                dl = learn.dls.test_dl(df, bs=4000)
                preds,_ = learn.get_preds(dl=dl)

                del dl

                class_idxs = preds.argmax(axis=1)

                class_probs= preds.max(axis=1)

                del preds

                class_probs=class_probs.values

                NumPred= class_idxs.tolist()
                PredProbs =class_probs.tolist()

                del class_idxs 
                del class_probs 

                res_df= pd.DataFrame(list(zip(NumPred, ID_l,PredProbs)),columns =['Pred_ID','ID','Prob'])

                del NumPred
                del PredProbs

                df_NAN['ID']= np.arange(len(df_NAN))

                df_NAN = df_NAN[['ID']]

                res_input_df = pd.merge(df_NAN,res_df, how='left', on = 'ID')

                Pred_arr = np.asarray(res_input_df['Pred_ID'])

                Pred_arr=Pred_arr+1

                Prob_arr = np.asarray(res_input_df['Prob'])
                Prob_ras = Prob_arr.reshape(arr.shape[1], arr.shape[2])

                Pred_ras = Pred_arr.reshape(arr.shape[1], arr.shape[2])

                if os.path.isdir("../Output/Pred/Batch/" + learn_i + '/') == False:
                    os.mkdir("../Output/Pred/Batch/" + learn_i + '/')

                # export
                driver = gdal.GetDriverByName("GTiff")
                driver.Register()
                outds = driver.Create("../Output/Pred/Batch/" + learn_i + '/' + img_i + '_' + learn_i +"_prob.tif", xsize = Prob_ras.shape[1],
                                    ysize = Prob_ras.shape[0], bands = 1, 
                                    eType = gdal.GDT_Float32)

                outds.SetGeoTransform(gt)
                outds.SetProjection(proj)
                outband = outds.GetRasterBand(1)
                outband.WriteArray(Prob_ras)
                outband.SetNoDataValue(65535)
                outband.FlushCache()

                # close your datasets and bands!!!
                outband = None
                outds = None

                driver = gdal.GetDriverByName("GTiff")
                driver.Register()
                outds = driver.Create("../Output/Pred/Batch/" + learn_i + '/'+ img_i + '_' + learn_i +"_pred.tif", xsize = Pred_ras.shape[1],
                                    ysize = Pred_ras.shape[0], bands = 1, 
                                    eType = gdal.GDT_Int16)
                outds.SetGeoTransform(gt)
                outds.SetProjection(proj)
                outband = outds.GetRasterBand(1)
                outband.WriteArray(Pred_ras)
                outband.SetNoDataValue(65535)
                outband.SetNoDataValue(32767)
                outband.FlushCache()
                # close your datasets and bands!!!
                outband = None
                outds = None

                gc.collect()
        del models_i
    print("The prediction has been done on all images provided")

