import qrcode
import requests
import pyautogui

#Folder to save qr code images to
folder = 'qr_wallets'


#Call this to clear screen for Windows, Linux, PyCharm
def clear_screen():
    # os.system('cls' if os.name == 'nt' else 'clear')
    #clear screen in PyCharm
    pyautogui.hotkey('ctrl', 'l')

#Call API to retrieve list of Top 10 cryptos
def get_top_10_cryptos():
    top_10_list = []
    r = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1&sparkline=false')
    r_dict = r.json()

    for item in r_dict:
        crypto_dict = {}

        crypto_dict['id'] = item.get('id')
        crypto_dict['name'] = item.get('name')
        crypto_dict['symbol'] = item.get('symbol')
        crypto_dict['rank'] = item.get('market_cap_rank')
        crypto_dict['ticker'] = str(item.get('name')) + ' ({})'.format(item.get('symbol').upper())

        top_10_list.append(crypto_dict)
    return top_10_list

#Define qr class
def create_qr_class():
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=15,
        border=1
    )
    return qr

#Takes in qr class object, list of top 10 cryptos, and selection (based on rank)
def create_qr_wallet(qr, cryptos, select):
    for item in cryptos:
        if item.get('rank') == select:
            filename = '{}_wallet.png'.format(item.get('name'))
            destination = folder + '/' + filename

            data = input('Enter a ' + item.get('ticker') + ' wallet address: ')

            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill='black', back_color='white')
            img.save(destination)
            qr.clear()
            break


#Print out menu for selecting a crypto
def print_menu(cryptos):
    print('Create QR Code Wallets for Top 10 Cryptocurrencies')
    for item in cryptos:
        print("{}. ".format(item.get('rank')) + str(item.get('ticker')))
    print()
    print('0. Exit Program')
    print()




def main():
    cryptos = get_top_10_cryptos()
    qr = create_qr_class()

    menu = True
    while (menu):
        print_menu(cryptos)
        select = input('Select a cryptocurrency to create a QR code wallet for: ')
        clear_screen()

        if 1 <= int(select) <= 10:
            create_qr_wallet(qr, cryptos, select)

        elif select == 0:
            print('Program Terminated')
            menu = False
        else:
            print('Invalid selection, select (1-10)')

    #Verify QR code is correct at url
    decode_qr_url = "https://zxing.org/w/decode.jspx"


if __name__ == "__main__":
    main()