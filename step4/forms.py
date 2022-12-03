class ReviewForm(forms.ModelForm):   
    class Meta:
        model = Review
        fields = ['score', 'comment']
from .models import Category, Pref, User, Review
from .models import Pref, Category, Review
from .forms import SearchForm, SignUpForm, LoginForm, ReviewForm
from django.db.models import Avg
def ShopInfo(request, restid):
    keyid = get_keyid()
    id = restid
    query = get_gnavi_data(id, "", "", "", 1)
    res_list = rest_search(query)
    restaurants_info = extract_restaurant_info(res_list)

    # 以下を追加、編集　ここから
    review_count = Review.objects.filter(shop_id=restid).count()
    score_ave = Review.objects.filter(shop_id = restid).aggregate(Avg('score'))
    average = score_ave['score__avg']
    if average:
        average_rate = average / 5 * 100
    else:
        average_rate = 0

    if request.method == 'GET':        
        review_form = ReviewForm()
        review_list = Review.objects.filter(shop_id = restid)

    else:
        form = ReviewForm(data=request.POST)
        score = request.POST['score']
        comment = request.POST['comment']

        if form.is_valid():
            review = Review()
            review.shop_id = restid
            review.shop_name = restaurants_info[0][1]
            review.shop_kana = restaurants_info[0][2]
            review.shop_address = restaurants_info[0][7]
            review.image_url = restaurants_info[0][5]
            review.user = request.user
            review.score = score
            review.comment = comment
            review.save()
            return redirect('techapp:shop_info', restid)
        else:
            return redirect('techapp:shop_info', restid)
        return render(request, 'techapp/index.html', {})

    params = {
        'title': '店舗詳細',
        'review_count': review_count,
        'restaurants_info': restaurants_info,
        'review_form': review_form,
        'review_list': review_list,
        'average': average,
        'average_rate': average_rate,
        }

    return render (request, 'techapp/shop_info.html', params)
    # 以下を追加、編集　ここまで
score_ave = Review.objects.filter(shop_id = restid).aggregate(Avg('score'))
