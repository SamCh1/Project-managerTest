from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Khởi tạo trình duyệt
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

try:
    # Mở trang web (đặt URL của trang web chứa đoạn HTML trên)
    driver.get('http://localhost:3000')

    # Đợi một chút để đảm bảo trang tải hoàn toàn
    time.sleep(3)

    # Tìm nút tìm kiếm và click vào nó
    # Thay 'search-button-id' bằng ID thực của nút tìm kiếm
    search_button = driver.find_element(
        By.CSS_SELECTOR, 'body > header > div > div > div.col-5 > form > div > button')
    search_button.click()

    # Đợi một chút để đảm bảo kết quả tìm kiếm tải hoàn toàn
    time.sleep(3)

    # Tìm tất cả các sản phẩm
    product_items = driver.find_elements(By.CLASS_NAME, 'product-item')

    # In thông tin về từng sản phẩm
    for product in product_items:
        title = product.find_element(By.CLASS_NAME, 'inner-title').text
        price_new = product.find_element(By.CLASS_NAME, 'inner-price-new').text
        price_old = product.find_element(By.CLASS_NAME, 'inner-price-old').text
        discount = product.find_element(By.CLASS_NAME, 'inner-discount').text
        print(
            f"Title: {title}, New Price: {price_new}, Old Price: {price_old}, Discount: {discount}")

finally:
    # Đóng trình duyệt
    driver.quit()
