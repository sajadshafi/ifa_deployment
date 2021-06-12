from django.http import request
from django.shortcuts import render
from .models import AprDrugDescription
import joblib
import pandas as pd

def index_view(requests):

    '''
        uncomment these lines and put your own csv file of drug description here and run the app it will add all the records of the drug description in the table
        Dont forget to make the model and run migrations

        # apr_df = pd.read_csv("/home/aladdin/Documents/ExcelR/Projects/Fraud Analysis/insurance_fraud_analysis/home/csv_files/drug_desc.csv")
        # list_of_description = list(apr_df["apr_drug_description"])

        # for item in list_of_description:
        #     AprDrugDescription.objects.create(apr_drg_description = item)
    '''
    list_of_description = AprDrugDescription.objects.all()
    if requests.method == "POST":
        X_input = {
            'Area_Service': requests.POST.get("area_service"),
            'Age': requests.POST.get("age"),
            'Gender': requests.POST.get("gender"),

            'Cultural_group': requests.POST.get("cultural_group"),
            'ethnicity': requests.POST.get("ethnicity"),
            'Days_spend_hsptl': requests.POST.get("days_in_hsptl"),

            'Admission_type': requests.POST.get("admission_type"),
            'Home or self care,': requests.POST.get("care_type"),
            'ccs_diagnosis_code': requests.POST.get("ccs_diag_code"),

            'ccs_procedure_code': requests.POST.get("ccs_procedure_code"),
            'Code_illness': requests.POST.get("code_illness"),
            'apr_drg_description': requests.POST.get("apr_drg_description"),

            'Mortality risk': requests.POST.get("mortality_risk"),
            'Surg_Description': requests.POST.get("surgery_desc"),
            'Emergency dept_yes/No': requests.POST.get("emergency"),

            'Tot_charg': requests.POST.get("total_charg"),
            'Tot_cost': requests.POST.get("total_cost"),
            'Payment_Typology': requests.POST.get("payment_typology")

        }

        prediction = "Genuine"
        predicted_value = predict_result(X_input)
        if predicted_value == 1:
            prediction = "Genuine"
        else:
            prediction = "Fraud"

        return render(requests, "home/index.html", {'drg_desc': list_of_description, "predicted_value": prediction})
    
    else:
        list_of_description = AprDrugDescription.objects.all()
        return render(requests, "home/index.html", {'drg_desc': list_of_description})


def predict_result(data):

    # Importing model and encoders from the files.
    encoders = joblib.load("/home/aladdin/Documents/ifa_project/insurance_fraud_analysis/home/ds_models/encoders.pkl")
    model = joblib.load("/home/aladdin/Documents/ifa_project/insurance_fraud_analysis/home/ds_models/random_forest.pkl")
    
    # Picking up categorical columns from the data recieved from the form
    cat = ['Area_Service', 'Age', 'Gender', 'Cultural_group', 'ethnicity',
        'Admission_type', 'Home or self care,', "apr_drg_description",
        'Surg_Description', 'Emergency dept_yes/No']


    # converting Recieved data into a dataframe
    input_data = pd.DataFrame(data, index=[0])
    input_data.reset_index().drop(columns = ["index"])


    for column in input_data.columns:
        if column in cat:
            input_data[column] = encoders[column].transform(input_data[column])
            input_data[column] = input_data[column].astype(int)

        else:
            input_data[column] = input_data[column].astype(int)

    predicted_value = model.predict(input_data)
    
    return predicted_value
