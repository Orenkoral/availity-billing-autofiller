import tkinter as tk
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tkinter import filedialog as fd
from tkinter import messagebox


# To utilize Selenium's webdriver function, it is required to download chromedriver on your web browser.
web = webdriver.Chrome(executable_path= r"your_chromedriver_path")


# I used the tkinter package to set up a graphical user interface for the billing application.
def gui_init(btn_cmd_two, btn_cmd):
    window = tk.Tk()
    window.title("Auto-Biller")

    for i in range(3):
        window.columnconfigure(i, weight=1, minsize=75)
        window.rowconfigure(i, weight=1, minsize=50)

    first_label = tk.Label(text = "First Name")
    second_label = tk.Label(text = "Last Name")

    global first_entry
    first_entry = tk.Entry(fg="black", bg="white", width=50)
    global second_entry
    second_entry = tk.Entry(fg="black", bg="white", width=50)
    
    button = tk.Button(
    window,
    text="Submit",
    width=25,
    height=5,
    bg="gray",
    fg="black",
    command = btn_cmd
    )
    
    choose_file = tk.Button(
    window,
    text="Choose File Path",
    width=15,
    height=2,
    bg="gray",
    fg="black",
    command = btn_cmd_two
    )
    
    first_label.pack()
    first_entry.pack()
    
    second_label.pack()
    second_entry.pack()
    
    button.pack()  
    choose_file.pack()
        
    window.mainloop()


def select_file():
    tk.Tk().withdraw()
    file = fd.askopenfilename(filetypes = (("excel files", "*.xlsx"),("all files","*.*")))
    messagebox.showinfo("File Uploaded", f"You have uploaded {file}")
    file_to_df = pd.read_excel(file)
    global df
    df = pd.DataFrame(file_to_df)
    df.iloc[: , 5] = df.iloc[: , 5].astype(str)
    df.iloc[:, 10] = df.iloc[:, 10].astype(str)
    

def availity_log():
    global url
    url = web.get("https://apps.availity.com/public/apps/home/#!/loadApp?appUrl=%2Fweb%2Fpre-claim%2Fclaims-correction-ui%2F%3FcacheBust%3D1642521978%23%2F34579779%2F95964%2Fprofessional")
    url
    time.sleep(2)
    user = "******"
    password = "******"
    user_input = web.find_element(By.XPATH, '//*[@id="userId"]')
    user_input.send_keys(user)
    pass_input = web.find_element(By.XPATH, '//*[@id="password"]')
    pass_input.send_keys(password)
    login = web.find_element(By.XPATH, '//*[@id="loginFormSubmit"]')
    login.click()
    web.maximize_window()
    web.implicitly_wait(20)

availity_log()


def iframer():
    iframe = web.find_element(By.XPATH, '//*[@id="newBodyFrame"]')
    web.switch_to.frame(iframe)
    web.implicitly_wait(20)
    
iframer()

def availity_filler():
    # Search function to pull up patient data
    try:  
        search = df[df["First Name"].str.contains(first_entry.get().upper())][df["Last Name"].str.contains(second_entry.get().upper())]
    except NameError:
        messagebox.showerror("Error", "Please select a valid file path or patient name!")
    
    search = df[df["First Name"].str.contains(first_entry.get().upper())][df["Last Name"].str.contains(second_entry.get().upper())]
       
    # Autofill patient data based on previous search function  
    try:
        last = search.iloc[0, 4]
        last_input = web.find_element(By.XPATH, '//*[@id="patient.name.last"]')
        last_input.send_keys(last)
    except IndexError:
        messagebox.showerror("Error", "Invalid patient name! Make sure to check for errors in the excel file.")
    
    first = search.iloc[0, 2]
    first_input = web.find_element(By.XPATH, '//*[@id="patient.name.first"]')
    first_input.send_keys(first)
    
    address = search.iloc[0, 12]
    address_input = web.find_element(By.XPATH, '//*[@id="patient.address.address1"]')
    address_input.send_keys(address)
    
    city = search.iloc[0, 14]
    city_input = web.find_element(By.XPATH, '//*[@id="patient.address.city"]')
    city_input.send_keys(city)
    
    state = search.iloc[0, 15]
    state_input = web.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[2]/div/div[2]/div/div[4]/div[2]/div/div[1]/div/div[1]/div[2]/div/input')
    state_input.send_keys(state, Keys.ENTER)
    
    zipcode = search.iloc[0, 16].astype(str)
    zipcode_input = web.find_element(By.XPATH, '//*[@id="patient.address.zipCode"]')
    zipcode_input.send_keys(zipcode)
    
    dob = search.iloc[0, 5]
    dob_input = web.find_element(By.XPATH, '//*[@id="patientbirthDate-btn"]')
    dob_input.send_keys(dob)
    
    gender = search.iloc[0, 6]
    gender_input = web.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[2]/div/div[2]/div/div[5]/div[3]/div/div[1]/div/div[1]/div[2]/div/input')
    gender_input.send_keys(gender)
    if gender == "M":
        gender_male = web.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[2]/div/div[2]/div/div[5]/div[3]/div/div[1]/div[2]/div/div[2]')
        gender_male.click()
    else:
        gender_female = web.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[2]/div/div[2]/div/div[5]/div[3]/div/div[1]/div[2]/div/div[1]')
        gender_female.click()
        
    
    temp_id = search.iloc[0, 9].astype(int)
    temp_id_input = web.find_element(By.XPATH, '//*[@id="subscriber.memberId"]')
    temp_id_input.send_keys(temp_id.astype(str))

    # Autofill constant availity elements
    plan_to_remit = "Yes"
    plan_to_remit_input = web.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[3]/div[2]/div[1]/div[3]/div/div[1]/div/div[1]/div[2]/div/input')
    plan_to_remit_input.send_keys(plan_to_remit, Keys.ENTER)
    
    provider_clicker = web.find_element(By.XPATH, '//*[@id="root"]/div/div/div/form/div[5]/div[2]/div[1]/div[1]/div/div[1]/div/div[1]/div[1]')
    provider_clicker.click()
    provider_input = web.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[5]/div[2]/div[1]/div[1]/div/div[1]/div[2]/div/div')
    provider_input.click()
    
    provider_address_clicker = web.find_element(By.XPATH, '//*[@id="root"]/div/div/div/form/div[5]/div[2]/div[1]/div[2]/div/div[1]/div/div[1]/div[1]')
    provider_address_clicker.click()
    provider_address_input = web.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[5]/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/div')
    provider_address_input.click()
    
    specialty_code = "*******"
    specialty_code_input = web.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[5]/div[2]/div[2]/div[2]/div/div[1]/div/div[1]/div[2]/div/input')
    specialty_code_input.send_keys(specialty_code)
    time.sleep(1)
    specialty_code_clicker = web.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[5]/div[2]/div[2]/div[2]/div/div[1]/div[2]/div/div')
    specialty_code_clicker.click()
    # WebDriverWait(web, 100).until(EC.element_to_be_selected((specialty_code_clicker))).click()
    
    
    billing_provider = "*******"
    billing_provider_input = web.find_element(By.XPATH, '//*[@id="billingProvider.ein"]')
    billing_provider_input.send_keys(billing_provider)
    
    diagnosis_code = "*******"
    diagnosis_code_input = web.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[10]/div[2]/div[1]/div[1]/div/div[1]/div/div[1]/div[2]/div/input')
    diagnosis_code_input.send_keys(diagnosis_code)
    time.sleep(1)
    diagnosis_code_clicker = web.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[10]/div[2]/div[1]/div[1]/div/div[1]/div[2]/div/div')
    diagnosis_code_clicker.click()
    
    patient_cn = "*******"
    patient_cn_input = web.find_element(By.XPATH, '//*[@id="claimInformation.controlNumber"]')
    patient_cn_input.send_keys(patient_cn)
    
    service_place = "*******"
    service_place_one_input = web.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[11]/div[2]/div[1]/div[1]/div[3]/div/div[1]/div/div[1]/div[2]/div/input')
    service_place_one_input.send_keys(service_place)
    web.implicitly_wait(20)
    service_place_one_clicker = web.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[11]/div[2]/div[1]/div[1]/div[3]/div/div[1]/div[2]/div/div')
    service_place_one_clicker.click()
    
    info_release_clicker = web.find_element(By.XPATH, '//*[@id="root"]/div/div/div/form/div[11]/div[2]/div[1]/div[3]/div[3]/div/div[1]/div/div[1]/div[1]')
    info_release_clicker.click()
    info_release_input = web.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[11]/div[2]/div[1]/div[3]/div[3]/div/div[1]/div[2]/div/div[2]')
    info_release_input.click()
    
    provider_signature_clicker = web.find_element(By.XPATH, '//*[@id="root"]/div/div/div/form/div[11]/div[2]/div[1]/div[4]/div[1]/div/div[1]/div[1]/div[1]/div[1]')
    provider_signature_clicker.click()
    provider_signature_input = web.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[11]/div[2]/div[1]/div[4]/div[1]/div/div[1]/div[2]/div/div[1]')
    provider_signature_input.click()
    
    auth_number = "*******"
    auth_number_one = web.find_element(By.XPATH, '//*[@id="claimInformation.priorAuthorizationNumber"]')
    auth_number_one.send_keys(auth_number)
    
    clia_num_input = web.find_element(By.XPATH, '//*[@id="claimInformation.clinicalLaboratoryImprovementAmendmentNumber"]')
    clia_num_input.send_keys(auth_number)
    
    # Row 1 Procedure Code
    service_two_input = web.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[11]/div[2]/div[2]/div/div[2]/div[1]/div[2]/div/div[1]/div/div[1]/div[2]/div/input')
    service_two_input.send_keys(service_place)
    web.implicitly_wait(20)
    service_two_clicker = web.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[11]/div[2]/div[2]/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/div')
    service_two_clicker.click()
    
    service_start = search.iloc[0, 10]
    service_start_first = web.find_element(By.XPATH, '//*[@id="claimInformationserviceLinesExpanded0fromDate-btn"]')
    service_start_first.send_keys(service_start)
    
    service_end_first = web.find_element(By.XPATH, '//*[@id="claimInformationserviceLinesExpanded0toDate-btn"]')
    service_end_first.send_keys(service_start)
    
    procedure_code_one = "*******"
    procedure_one_input = web.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[11]/div[2]/div[2]/div/div[2]/div[3]/div[1]/div/div[1]/div/div[1]/div[2]/div/input')
    procedure_one_input.send_keys(procedure_code_one)
    time.sleep(1)
    procedure_one_clicker = web.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[11]/div[2]/div[2]/div/div[2]/div[3]/div[1]/div/div[1]/div[2]/div/div')
    procedure_one_clicker.click()
    
    charge_amount = "*******"
    charge_one = web.find_element(By.XPATH, '//*[@id="claimInformation.serviceLinesExpanded0.amount"]')
    charge_one.send_keys(charge_amount)
    
    qty = "*******"
    qty_one = web.find_element(By.XPATH, '//*[@id="claimInformation.serviceLinesExpanded0.quantity"]')
    qty_one.send_keys(qty)
    
    auth_number_two = web.find_element(By.XPATH, '//*[@id="claimInformation.serviceLinesExpanded0.priorAuthorizationNumber"]')
    auth_number_two.send_keys(auth_number)
    
    code_pointer_one = web.find_element(By.XPATH, '//*[@id="root"]/div/div/div/form/div[11]/div[2]/div[2]/div/div[2]/div[7]/div[1]/div/div[1]/div/div[1]/div[1]')
    code_pointer_one.click()
    code_pointer_one_input = web.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[11]/div[2]/div[2]/div/div[2]/div[7]/div[1]/div/div[1]/div[2]/div/div')
    code_pointer_one_input.click()
    
    clia_num_one = web.find_element(By.XPATH, '//*[@id="claimInformation.serviceLinesExpanded0.clinicalLaboratoryImprovementAmendmentNumber"]')
    clia_num_one.send_keys(auth_number)
    
    r_clia_num_one = web.find_element(By.XPATH, '//*[@id="claimInformation.serviceLinesExpanded0.referringClinicalLaboratoryImprovementAmendmentNumber"]')
    r_clia_num_one.send_keys(auth_number)
    
    add_row_two = web.find_element(By.XPATH, '//*[@id="root"]/div/div/div/form/div[11]/div[2]/div[3]/div[2]/button')
    add_row_two.click()
    
    # Row 2 Procedure Code
    service_place_three_input = web.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[11]/div[2]/div[3]/div/div[2]/div[1]/div[2]/div/div[1]/div/div[1]/div[2]/div/input')
    service_place_three_input.send_keys(service_place)
    web.implicitly_wait(20)
    service_place_three_clicker = web.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[11]/div[2]/div[3]/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/div')
    service_place_three_clicker.click()
    
    service_start_second = web.find_element(By.XPATH, '//*[@id="claimInformationserviceLinesExpanded1fromDate-btn"]')
    service_start_second.send_keys(service_start)
    
    service_end_second = web.find_element(By.XPATH, '//*[@id="claimInformationserviceLinesExpanded1toDate-btn"]')
    service_end_second.send_keys(service_start)
    
    procedure_code_two = "*******"
    procedure_two_input = web.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[11]/div[2]/div[3]/div/div[2]/div[3]/div[1]/div/div[1]/div/div[1]/div[2]/div/input')
    procedure_two_input.send_keys(procedure_code_two)
    time.sleep(1)
    procedure_two_clicker = web.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[11]/div[2]/div[3]/div/div[2]/div[3]/div[1]/div/div[1]/div[2]/div/div')
    procedure_two_clicker.click()
    
    charge_two = web.find_element(By.XPATH, '//*[@id="claimInformation.serviceLinesExpanded1.amount"]')
    charge_two.send_keys(charge_amount)
    
    qty_two = web.find_element(By.XPATH, '//*[@id="claimInformation.serviceLinesExpanded1.quantity"]')
    qty_two.send_keys(qty)
    
    auth_number_three = web.find_element(By.XPATH, '//*[@id="claimInformation.serviceLinesExpanded1.priorAuthorizationNumber"]')
    auth_number_three.send_keys(auth_number)
    
    code_pointer_two = web.find_element(By.XPATH, '//*[@id="root"]/div/div/div/form/div[11]/div[2]/div[3]/div/div[2]/div[7]/div[1]/div/div[1]/div/div[1]/div[1]')
    code_pointer_two.click()
    code_pointer_two_input = web.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[11]/div[2]/div[3]/div/div[2]/div[7]/div[1]/div/div[1]/div[2]/div/div')
    code_pointer_two_input.click()
    
    clia_num_two = web.find_element(By.XPATH, '//*[@id="claimInformation.serviceLinesExpanded1.clinicalLaboratoryImprovementAmendmentNumber"]')
    clia_num_two.send_keys(auth_number)
    
    r_clia_num_two = web.find_element(By.XPATH, '//*[@id="claimInformation.serviceLinesExpanded1.referringClinicalLaboratoryImprovementAmendmentNumber"]')
    r_clia_num_two.send_keys(auth_number)
    
    add_row_three = web.find_element(By.XPATH, '//*[@id="root"]/div/div/div/form/div[11]/div[2]/div[4]/div[2]/button')
    add_row_three.click()
    
    # Row 3 Procedure Code
    service_place_four_input = web.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[11]/div[2]/div[4]/div/div[2]/div[1]/div[2]/div/div[1]/div/div[1]/div[2]/div/input')
    service_place_four_input.send_keys(service_place)
    web.implicitly_wait(20)
    service_place_four_clicker = web.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[11]/div[2]/div[4]/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/div')
    service_place_four_clicker.click()
    
    service_start_third = web.find_element(By.XPATH, '//*[@id="claimInformationserviceLinesExpanded2fromDate-btn"]')
    service_start_third.send_keys(service_start)
    
    service_end_third = web.find_element(By.XPATH, '//*[@id="claimInformationserviceLinesExpanded2toDate-btn"]')
    service_end_third.send_keys(service_start)
    
    procedure_code_three = "*******"
    procedure_three_input = web.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[11]/div[2]/div[4]/div/div[2]/div[3]/div[1]/div/div[1]/div/div[1]/div[2]/div/input')
    procedure_three_input.send_keys(procedure_code_three)
    time.sleep(1)
    procedure_three_clicker = web.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[11]/div[2]/div[4]/div/div[2]/div[3]/div[1]/div/div[1]/div[2]/div/div')
    procedure_three_clicker.click()
    
    charge_three = web.find_element(By.XPATH, '//*[@id="claimInformation.serviceLinesExpanded2.amount"]')
    charge_three.send_keys(charge_amount)
    
    qty_three = web.find_element(By.XPATH, '//*[@id="claimInformation.serviceLinesExpanded2.quantity"]')
    qty_three.send_keys(qty)
    
    auth_number_four = web.find_element(By.XPATH, '//*[@id="claimInformation.serviceLinesExpanded2.priorAuthorizationNumber"]')
    auth_number_four.send_keys(auth_number)
    
    code_pointer_three = web.find_element(By.XPATH, '//*[@id="root"]/div/div/div/form/div[11]/div[2]/div[4]/div/div[2]/div[7]/div[1]/div/div[1]/div/div[1]/div[1]')
    code_pointer_three.click()
    code_pointer_three_input = web.find_element(By.XPATH, '//html/body/div[1]/div/div/div/form/div[11]/div[2]/div[4]/div/div[2]/div[7]/div[1]/div/div[1]/div[2]/div/div')
    code_pointer_three_input.click()
    
    clia_num_three = web.find_element(By.XPATH, '//*[@id="claimInformation.serviceLinesExpanded2.clinicalLaboratoryImprovementAmendmentNumber"]')
    clia_num_three.send_keys(auth_number)
    
    r_clia_num_three = web.find_element(By.XPATH, '//*[@id="claimInformation.serviceLinesExpanded2.referringClinicalLaboratoryImprovementAmendmentNumber"]')
    r_clia_num_three.send_keys(auth_number)
    
    add_row_four = web.find_element(By.XPATH, '//*[@id="root"]/div/div/div/form/div[11]/div[2]/div[5]/div[2]/button')
    add_row_four.click()
    
    # Row 4 Procedure Code
    service_place_five_input = web.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[11]/div[2]/div[5]/div/div[2]/div[1]/div[2]/div/div[1]/div/div[1]/div[2]/div/input')
    service_place_five_input.send_keys(service_place)
    web.implicitly_wait(20)
    service_place_five_clicker = web.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[11]/div[2]/div[5]/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/div')
    service_place_five_clicker.click()
    
    service_start_fourth = web.find_element(By.XPATH, '//*[@id="claimInformationserviceLinesExpanded3fromDate-btn"]')
    service_start_fourth.send_keys(service_start)
    
    service_end_fourth = web.find_element(By.XPATH, '//*[@id="claimInformationserviceLinesExpanded3toDate-btn"]')
    service_end_fourth.send_keys(service_start)
    
    procedure_code_four = "*******"  
    procedure_four_input = web.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[11]/div[2]/div[5]/div/div[2]/div[3]/div[1]/div/div[1]/div/div[1]/div[2]/div/input')
    procedure_four_input.send_keys(procedure_code_four)
    time.sleep(1)
    procedure_four_clicker = web.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[11]/div[2]/div[5]/div/div[2]/div[3]/div[1]/div/div[1]/div[2]/div/div')
    procedure_four_clicker.click()
    
    charge_four = web.find_element(By.XPATH, '//*[@id="claimInformation.serviceLinesExpanded3.amount"]')
    charge_four.send_keys(charge_amount)
    
    qty_four = web.find_element(By.XPATH, '//*[@id="claimInformation.serviceLinesExpanded3.quantity"]')
    qty_four.send_keys(qty)
    
    auth_number_five = web.find_element(By.XPATH, '//*[@id="claimInformation.serviceLinesExpanded3.priorAuthorizationNumber"]')
    auth_number_five.send_keys(auth_number)
    
    code_pointer_four = web.find_element(By.XPATH, '//*[@id="root"]/div/div/div/form/div[11]/div[2]/div[5]/div/div[2]/div[7]/div[1]/div/div[1]/div/div[1]/div[1]')
    code_pointer_four.click()
    code_pointer_four_input = web.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[11]/div[2]/div[5]/div/div[2]/div[7]/div[1]/div/div[1]/div[2]/div/div')
    code_pointer_four_input.click()
    
    clia_num_four = web.find_element(By.XPATH, '//*[@id="claimInformation.serviceLinesExpanded3.clinicalLaboratoryImprovementAmendmentNumber"]')
    clia_num_four.send_keys(auth_number)
    
    r_clia_num_four = web.find_element(By.XPATH, '//*[@id="claimInformation.serviceLinesExpanded3.referringClinicalLaboratoryImprovementAmendmentNumber"]')
    r_clia_num_four.send_keys(auth_number)
    
    add_row_five = web.find_element(By.XPATH, '//*[@id="root"]/div/div/div/form/div[11]/div[2]/div[6]/div[2]/button')
    add_row_five.click()
    
    # Row 5 Procedure Code
    service_place_six_input = web.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[11]/div[2]/div[6]/div/div[2]/div[1]/div[2]/div/div[1]/div/div[1]/div[2]/div/input')
    service_place_six_input.send_keys(service_place)
    web.implicitly_wait(20)
    service_place_six_clicker = web.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[11]/div[2]/div[6]/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/div')
    service_place_six_clicker.click()
    
    service_start_fifth = web.find_element(By.XPATH, '//*[@id="claimInformationserviceLinesExpanded4fromDate-btn"]')
    service_start_fifth.send_keys(service_start)
    
    service_end_fifth = web.find_element(By.XPATH, '//*[@id="claimInformationserviceLinesExpanded4toDate-btn"]')
    service_end_fifth.send_keys(service_start)
    
    procedure_code_five = "*******"  
    procedure_five_input = web.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[11]/div[2]/div[6]/div/div[2]/div[3]/div[1]/div/div[1]/div/div[1]/div[2]/div/input')
    procedure_five_input.send_keys(procedure_code_five)
    time.sleep(1)
    procedure_five_clicker = web.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[11]/div[2]/div[6]/div/div[2]/div[3]/div[1]/div/div[1]/div[2]/div/div')
    procedure_five_clicker.click()
    
    charge_five = web.find_element(By.XPATH, '//*[@id="claimInformation.serviceLinesExpanded4.amount"]')
    charge_five.send_keys(charge_amount)
    
    qty_five = web.find_element(By.XPATH, '//*[@id="claimInformation.serviceLinesExpanded4.quantity"]')
    qty_five.send_keys(qty)
    
    auth_number_six = web.find_element(By.XPATH, '//*[@id="claimInformation.serviceLinesExpanded4.priorAuthorizationNumber"]')
    auth_number_six.send_keys(auth_number)
    
    code_pointer_five = web.find_element(By.XPATH, '//*[@id="root"]/div/div/div/form/div[11]/div[2]/div[6]/div/div[2]/div[7]/div[1]/div/div[1]/div/div[1]/div[1]')
    code_pointer_five.click()
    code_pointer_five_input = web.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[11]/div[2]/div[6]/div/div[2]/div[7]/div[1]/div/div[1]/div[2]/div/div')
    code_pointer_five_input.click()
    
    clia_num_five = web.find_element(By.XPATH, '//*[@id="claimInformation.serviceLinesExpanded4.clinicalLaboratoryImprovementAmendmentNumber"]')
    clia_num_five.send_keys(auth_number)
    
    r_clia_num_five = web.find_element(By.XPATH, '//*[@id="claimInformation.serviceLinesExpanded4.referringClinicalLaboratoryImprovementAmendmentNumber"]')
    r_clia_num_five.send_keys(auth_number)

          
gui_init(select_file, availity_filler)