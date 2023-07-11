from booking.booking import Booking

bot = Booking()
bot.land_first_page()
bot.clear_popup()
bot.change_currency()
bot.select_place_to_go('Japan')
bot.select_dates(check_in_date='2023-07-24',
                 check_out_date='2023-08-04')
bot.select_adults(3)
bot.click_search()
bot.apply_filtration()
