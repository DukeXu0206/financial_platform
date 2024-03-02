from django.contrib import admin


from financialSystem.models import StockInfo, UserTable, HistoryTradeTable, News, StockComment, CommentReply

admin.site.site_header = 'Financial backend system'  # header
admin.site.site_title = 'Financial backend system'   # title
admin.site.index_title = 'Financial backend system'
# Register your models here.

admin.site.register(UserTable)
admin.site.register(HistoryTradeTable);
admin.site.register(StockComment);
admin.site.register(CommentReply);

@admin.register(StockInfo)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['stock_id','stock_name','issuance_time','closing_price_y','open_price_t','stock_type','block','change_extent']

@admin.register(News)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['title','source','content','news_dataTime']




