from django.shortcuts import render
from .models import AprDrugDescription

import pandas as pd

def index_view(requests):
    apr_df = pd.read_csv("/home/aladdin/Documents/ExcelR/Projects/Fraud Analysis/insurance_fraud_analysis/home/csv_files/drug_desc.csv")
    list_of_description = list(apr_df["apr_drug_description"])

    # for item in list_of_description:
    #     AprDrugDescription.objects.create(apr_drg_description = item)

    
    return render(requests, "home/index.html", {'drg_desc': list_of_description})
