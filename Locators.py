

class Locators:

    main_website = "https://www.supremenewyork.com"
    shop_page = "https://www.supremenewyork.com/shop"
    starting_page = ""
    checkout_page = "https://www.supremenewyork.com/checkout"
    formFieldIds = {
        "name": "order_billing_name",
        "email": "order_email",
        "tel": "order_tel",
        "address" : "bo",
        "unit": "oba3",
        "zip": "order_billing_zip",
        "city": "order_billing_city",
        "state": "order_billing_state",
        "country": "order_billing_country",
        "number": "nnaerb",
        "credit_month": "credit_card_month",
        "credit_year": "credit_card_year",
        "cvv": "orcer",
        "terms_spec": "iCheck-helper",
        "submit_css": "input[name='commit']"
    }


    shopListing_class = "shop"
    listingName_tag = "li"
    listingLink_tag = "a"
    productImg_Id = "img-main"
    product_name_css = {"itemprop" : "name"}
    product_price_css = "span[itemprop='price']"
    sizeOption_id = "s"
    style_name_css_key = "data-style-name"
    sold_out_class = "sold-out"
    addToCart_css = "input[value='add to cart']"
    button_checkout_linkT = "checkout now"
