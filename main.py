import requests, time, json, os, threading


def scrapeSizes(prod, sizes):
    list = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.newbalance.com/men/shoes/all-shoes/',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
        'TE': 'Trailers',
    }

    response = requests.get(prod, headers=headers).text
    l = response.split('{"variants":')[1].split("]}")[0] + "]"
    j = json.loads(l)
    for size in sizes:
        for x in j:
            if x['size'] == size:
                list.append(x['id'])
    return ['195173274867']


def atc(ses, pid):
    global uuid
    global start
    start = time.time()
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.newbalance.com/pd/fresh-foam-roav-tee-shirt/MROAVV1-30767-M.html/?ICID=HP_PDP_ROAV_TEE_SHIRT_11372_M',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    }

    data = {
        'pid': f'{pid}',
        'quantity': '1',
        'options': '[]'
    }

    response = ses.post('https://www.newbalance.com/on/demandware.store/Sites-NBUS-Site/en_US/Cart-AddProduct',  headers=headers, data=data).json()
    uuid = response['pliUUID']

def setShipping(ses, info):
    global name, lastName, address1, address2, city, state, postal, phone, email
    try:
        name = info['name']
        lastName = info['lastName']
        address1 = info['address1']
        address2 = info['address2']
        city = info['city']
        state = info['state']
        postal = info['postal']
        phone = info['phone']
        email = info['email']
    except:
        pass
    global csrf
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.newbalance.com/checkout-begin/?stage=shipping',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }
    response = ses.get("https://www.newbalance.com/checkout-begin/", headers=headers)
    csrf = response.text.split('<input type="hidden" name="csrf_token" value="')[1].split('"')[0]
    data = {
        'originalShipmentUUID': f'{uuid}',
        'shipmentUUID': f'{uuid}',
        'zipCodeErrorMsg': 'Please enter a valid Zip/Postal code',
        'shipmentSelector': 'new',
        'dwfrm_shipping_shippingAddress_addressFields_country': 'US',
        'dwfrm_shipping_shippingAddress_addressFields_firstName': '',
        'dwfrm_shipping_shippingAddress_addressFields_lastName': '',
        'dwfrm_shipping_shippingAddress_addressFields_address1': '',
        'dwfrm_shipping_shippingAddress_addressFields_address2': '',
        'dwfrm_shipping_shippingAddress_addressFields_city': '',
        'dwfrm_shipping_shippingAddress_addressFields_states_stateCode': 'NY',
        'dwfrm_shipping_shippingAddress_addressFields_postalCode': '',
        'dwfrm_shipping_shippingAddress_addressFields_phone': '(645) 680-9725',
        'dwfrm_shipping_shippingAddress_addressFields_email': '',
        'dwfrm_shipping_shippingAddress_addressFields_addtoemaillist': 'true',
        'dwfrm_shipping_shippingAddress_shippingMethodID': 'Ground',
        'csrf_token': f'{csrf}',
        'saveShippingAddr': 'false'
    }

    response = ses.post('https://www.newbalance.com/on/demandware.store/Sites-NBUS-Site/en_US/CheckoutShippingServices-SubmitShipping',headers=headers, data=data).json()

def setBillingCheckout(ses, info):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.newbalance.com/checkout-begin/?stage=payment',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    }

    data = [
        ('csrf_token', f'{csrf}'),
        ('localizedNewAddressTitle', 'New Address'),
        ('dwfrm_billing_paymentMethod', 'CREDIT_CARD'),
        ('dwfrm_billing_paymentMethod', 'CREDIT_CARD'),
        ('dwfrm_billing_paymentMethod', 'CREDIT_CARD'),
        ('dwfrm_billing_creditCardFields_cardNumber', '4767718416985960'),
        ('dwfrm_billing_creditCardFields_cardNumber', '4767718416985960'),
        ('dwfrm_billing_creditCardFields_expirationMonth', '12'),
        ('dwfrm_billing_creditCardFields_expirationMonth', '12'),
        ('dwfrm_billing_creditCardFields_expirationYear', '2026'),
        ('dwfrm_billing_creditCardFields_expirationYear', '2026'),
        ('dwfrm_billing_creditCardFields_securityCode', '110'),
        ('dwfrm_billing_creditCardFields_securityCode', '110'),
        ('dwfrm_billing_creditCardFields_cardType', 'Visa'),
        ('dwfrm_billing_creditCardFields_cardType', 'Visa'),
        ('dwfrm_billing_realtimebanktransfer_iban', ''),
        ('dwfrm_billing_realtimebanktransfer_iban', ''),
        ('dwfrm_afterpay_isAfterpayUrl', '/on/demandware.store/Sites-NBUS-Site/en_US/AfterpayRedirect-IsAfterpay'),
        ('dwfrm_afterpay_redirectAfterpayUrl', '/on/demandware.store/Sites-NBUS-Site/en_US/AfterpayRedirect-Redirect'),
        ('dwfrm_billing_shippingAddressUseAsBillingAddress', 'true'),
        ('addressSelector', f'{uuid}'),
        ('dwfrm_billing_addressFields_country', 'US'),
        ('dwfrm_billing_addressFields_firstName', ''),
        ('dwfrm_billing_addressFields_lastName', ''),
        ('dwfrm_billing_addressFields_address1', ''),
        ('dwfrm_billing_addressFields_address2', ''),
        ('dwfrm_billing_addressFields_city', ''),
        ('dwfrm_billing_addressFields_states_stateCode', ''),
        ('dwfrm_billing_addressFields_postalCode', ''),
        ('dwfrm_billing_addressFields_phone', '1646581635'),
        ('', ''),
        ('addressId', f'{uuid}'),
        ('saveBillingAddr', 'false'),
    ]

    response = ses.post('https://www.newbalance.com/on/demandware.store/Sites-NBUS-Site/en_US/CheckoutServices-SubmitPayment',headers=headers, data=data)
    print("Billing set.")
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.newbalance.com/checkout-begin/?stage=placeOrder',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    }

    params = (
        ('termsconditions', 'undefined'),
    )

    response = ses.post(
        'https://www.newbalance.com/on/demandware.store/Sites-NBUS-Site/en_US/CheckoutServices-PlaceOrder',
        headers=headers, params=params).json()
    end = time.time()
    if response['error']:
        print("Total task took: " + str(round((end - start), 2)) + "seconds.")
        return "Failure checking out, possible card decline."
    return "Possible Check Out."

def createProfile():
    profile = {
        "profileName": input("Profile name: "),
        "name": input("First Name: "),
        "lastName": input('Last Name: '),
        "address1": input("Address 1: "),
        "address2": input("Address 2(simply leve blank for none): "),
        "city": input("City: "),
        "state": input("State: "),
        "postal": input("Postal: "),
        "phone": input("Phone: "),
        "email": input('Email: '),
        "cardType": input("Card Type: "),
        "cardNum": input("Card Number(data is saved locally in JSON format, fully client-sided): "),
        "cardExpMonth": input("Card Expiration Month: "),
        "cardExpYear": input("Card Expiration Year: "),
        "cvv": input("CVV: ")


    }
    fname = "profiles.json"
    if os.path.isfile(fname):
        # File exists
        with open(fname, 'a+') as outfile:
            with open(fname, 'rb+') as outfile2:
                outfile2.seek(-1, os.SEEK_END)
                outfile2.truncate()
            outfile.write(',')
            json.dump(profile, outfile)
            outfile.write(']')
    else:
        # Create file
        with open(fname, 'w') as outfile:
            array = []
            array.append(profile)
            outfile.write(str(array).replace("'", '"'))

def task(prof, pid):
    s = requests.session()
    atc(s, pid)
    setShipping(s, prof)
    print(setBillingCheckout(s, prof))

def createTasks(profile, prod, sizes):
    vars = scrapeSizes(prod, sizes)
    print(vars)
    sizeDiv = int(str(float(tasks / len(sizes))).split(".")[0])
    jobs = []
    for x in range(sizeDiv):
        for var in vars:
            t = jobs.append(threading.Thread(target=task, args=(profile, var)))
    # start  threads
    for j in jobs:
        j.start()

if __name__ == '__main__':
    global tasks
    global product
    print("NewBalance bot by evan.")
    inp = input("Would you like to: \n1. Create a profile \n2. Create tasks\n")
    if inp == '1':
        createProfile()
    if inp == '2':
        with open('profiles.json') as f:
            data = json.load(f)
            productLink = input("Please input a product link. \n")
            s = input("Please input size/size range(seperated by comma with no spaces)\n")
            sizes = s.split(",")
            tasks = int(input("How many tasks would you like to create?\n"))
            print("Which profile would you like to create tasks with?")
            for profile in data:
                print(profile['profileName'])
            prof = input("Enter a profile name: ")
            for profile in data:
                if profile['profileName'] == prof:
                    createTasks(prof, productLink, sizes)

