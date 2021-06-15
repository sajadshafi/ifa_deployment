import joblib
import pandas as pd

from django.http import request
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import AprDrugDescription


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
    
    return render(requests, "home/index.html", {'drg_desc': list_of_description})


def predict_result(data):

    # Importing model and encoders from the files.
    encoders = joblib.load("C:\\Users\\Malik\\Documents\\ifa_project\\insurance_fraud_analysis\\home\\ds_models\\encoders.pkl")
    model = joblib.load("C:\\Users\\Malik\\Documents\\ifa_project\\insurance_fraud_analysis\\home\\ds_models\\random_forest.pkl")
    
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


def ajax_prediction(request):
    if request.method == "POST":
        X_input = {
            'Area_Service': request.POST['area_service'],
            'Age': request.POST["age"],
            'Gender': request.POST["gender"],

            'Cultural_group': request.POST["cultural_group"],
            'ethnicity': request.POST["ethnicity"],
            'Days_spend_hsptl': request.POST["days_spend_hsptl"],

            'Admission_type': request.POST["admission_type"],
            'Home or self care,': request.POST["care_type"],
            'ccs_diagnosis_code': request.POST["ccs_diag_code"],

            'ccs_procedure_code': request.POST["ccs_procedure_code"],
            'Code_illness': request.POST["code_illness"],
            'apr_drg_description': request.POST["apr_drg_description"],

            'Mortality risk': request.POST["mortality_risk"],
            'Surg_Description': request.POST["surg_description"],
            'Emergency dept_yes/No': request.POST["emergency"],

            'Tot_charg': request.POST["total_charges"],
            'Tot_cost': request.POST["total_cost"],
            'Payment_Typology': request.POST["payment_typology"]

        }

        prediction = "Unknown"
        predicted_value = predict_result(X_input)
        if predicted_value == 1:
            prediction = "Genuine"
        else:
            prediction = "Fraud"

        print(prediction)
    
    return HttpResponse(prediction)

