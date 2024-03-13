from django.contrib import admin

from financial_system.models import *

admin.site.site_header = 'Financial System Backend'  # header
admin.site.site_title = 'Financial System Backend'  # title
admin.site.index_title = 'Financial System Backend'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'phone_number', 'user_email', 'account_balance', 'user_gender')


@admin.register(HistoryTrade)
class HistoryTradeAdmin(admin.ModelAdmin):
    list_display = ('get_user_name', 'get_stock_symbol', 'trade_type', 'trade_price', 'trade_quantity', 'trade_dateTime')

    def get_user_name(self, obj):
        return obj.user_id.user_name
    get_user_name.admin_order_field = 'user_id'  # Allows column order sorting
    get_user_name.short_description = 'User Name'  # Renames column head

    def get_stock_symbol(self, obj):
        return obj.stock_symbol.symbol
    get_stock_symbol.admin_order_field = 'stock_symbol__symbol'  # Allows column order sorting
    get_stock_symbol.short_description = 'Stock Symbol'  # Renames column head


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('get_user_name', 'get_stock_symbol')
    list_filter = ('user_id__user_name', 'stock_symbol__symbol')
    search_fields = ('user_id__user_name', 'stock_symbol__symbol')

    def get_user_name(self, obj):
        return obj.user_id.user_name
    get_user_name.admin_order_field = 'user_id'  # Allows column order sorting
    get_user_name.short_description = 'User Name'  # Sets column header

    def get_stock_symbol(self, obj):
        return obj.stock_symbol.symbol
    get_stock_symbol.admin_order_field = 'stock_symbol__symbol'  # Allows column order sorting
    get_stock_symbol.short_description = 'Stock Symbol'  # Sets column header


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'get_company_name', 'currency', 'get_exchange_name', 'timezone', 'get_first_trade_date')

    def get_exchange_name(self, obj):
        return obj.exchangeName
    get_exchange_name.admin_order_field = 'exchangeName'
    get_exchange_name.short_description = 'Exchange Name'  # Custom column header

    def get_first_trade_date(self, obj):
        date_time_obj = datetime.fromtimestamp(obj.firstTradeDate)
        return date_time_obj.strftime('%Y-%m-%d')
    get_first_trade_date.admin_order_field = 'firstTradeDate'
    get_first_trade_date.short_description = 'First Trade Date'  # Custom column header

    def get_company_name(self, obj):
        return obj.get_company_name()

    get_company_name.short_description = 'Company Name'


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'type', 'get_provider_publish_time', 'get_related_tickers', 'link')

    def get_provider_publish_time(self, obj):
        return obj.providerPublishTime.strftime('%Y-%m-%d %H:%M:%S')

    get_provider_publish_time.admin_order_field = 'providerPublishTime'
    get_provider_publish_time.short_description = 'Publish Time'  # Sets the column header

    def get_related_tickers(self, obj):
        return obj.relatedTickers
    get_related_tickers.short_description = 'Related Tickers'  # Sets the column header


@admin.register(StockComment)
class StockCommentAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_user_name', 'get_stock_symbol', 'comment_time', 'short_content')

    def get_user_name(self, obj):
        # Assuming User model has a field 'username' or similar for display
        return obj.user_id.user_name

    get_user_name.admin_order_field = 'user_id'  # Allows column order sorting
    get_user_name.short_description = 'User'  # Sets column header

    def get_stock_symbol(self, obj):
        # Assuming Stock model has a field 'symbol'
        return obj.stock_symbol.symbol

    get_stock_symbol.admin_order_field = 'stock_symbol__symbol'  # Allows column order sorting
    get_stock_symbol.short_description = 'Stock Symbol'  # Sets column header

    def short_content(self, obj):
        # Display first 50 characters of the comment's content
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content

    short_content.short_description = 'Content Preview'  # Sets column header


@admin.register(UserNotification)
class UserNotificationAdmin(admin.ModelAdmin):
    list_display = ('get_user_name', 'title', 'short_message', 'read', 'created_at')
    list_filter = ('read', 'created_at', 'user__user_name')
    search_fields = ('title', 'message', 'user__user_name')

    def get_user_name(self, obj):
        return obj.user.user_name
    get_user_name.admin_order_field = 'user'  # Allows column order sorting
    get_user_name.short_description = 'User'  # Sets column header

    def short_message(self, obj):
        # Display first 50 characters of the notification's message
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message
    short_message.short_description = 'Message Preview'  # Sets column header


# admin.site.register(CommentReply)