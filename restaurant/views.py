from django.http import JsonResponse
from django.shortcuts import render,redirect
from .models import Restaurant
from django.db.models import Q
from math import radians, sin, cos, sqrt, atan2
from geopy.geocoders import Nominatim

def get_lat_long(location):
    # Create a geolocator object
    geolocator = Nominatim(user_agent="my_app")

    try:
        # Geocode the location
        location = geolocator.geocode(location)
        
        if location:
            return location.latitude, location.longitude
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None




def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth's radius in kilometers

    # Convert latitude and longitude to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c

    return distance  # Distance in kilometers


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        data=Restaurant.objects.all()
        if 'term' in request.GET:
            item=request.GET.get('term').lower()
            qs=Restaurant.objects.all()
            items_list=list()
            for q in qs:
                for i in q.items.keys():
                    if i.lower().startswith(item):
                        if i not in items_list:
                            items_list.append(i)
            return JsonResponse(items_list,safe=False)
        if request.method=="GET" and "search" in request.GET:
            searched_item=request.GET["search"].title()
            try:
                results = Restaurant.objects.filter(Q(items__has_key=searched_item))
                # lat1=location_object.latitude
                # lon1=location_object.longitude
                # coordinates=get_lat_long(f"{request.user.location},Bangalore,India")    
                coordinates=get_lat_long(f"{request.user.location},Bangalore,India")    
                if coordinates:
                    lat1, lon1 = coordinates
                else:
                    print("Location not found or an error occurred.")
                lst={}
                for result in results:
                    lat2=result.latitude
                    lon2=result.longitude
                    try:
                        distance = haversine_distance(lat1, lon1, lat2, lon2)
                        if distance<=1:
                            score_distance=10
                        elif 1<distance<=2:
                            score_distance=9
                        elif 2<distance<=3:
                            score_distance=8
                        elif 3<distance<=4:
                            score_distance=7
                        elif 4<distance<=5:
                            score_distance=6
                        elif 5<distance<=6:
                            score_distance=5
                        elif 6<distance<=7:
                            score_distance=4
                        elif 7<distance<=8:
                            score_distance=3
                        elif 8<distance<=9:
                            score_distance=2
                        elif 9<distance<=10:
                            score_distance=1
                        elif distance>10:
                            score_distance=0
                    except:
                        distance=0
                        score_distance=0
                    try:
                        price=float(result.items[searched_item].replace("onwards",""))
                        if price<=100:
                            score_price=5
                        elif 100<price<=200:
                            score_price=4
                        elif 200<price<=300:
                            score_price=3
                        elif 300<price<=400:
                            score_price=2
                        elif 400<price<=500:
                            score_price=1
                        else:
                            score_price=0             
                    except Exception as e:
                        print(e)
                        price=0
                        score_price=0
                        
                    try:
                        rating=float(result.full_details["user_rating"]["aggregate_rating"])
                        if rating>=5:
                            score_rating=5
                        elif 4<=rating<5:
                            score_rating=4
                        elif 3<=rating<4:
                            score_rating=3
                        elif 2<=rating<3:
                            score_rating=2
                        elif 1<=rating<2:
                            score_rating=1
                        elif rating<1:
                            score_rating=0
                    except:
                        rating=0
                        score_rating=0
                    total_score=score_distance+score_price+score_rating
                    lst[result]=(distance,total_score)
                try:
                    sorted_restaurants = list(sorted(lst.items(), key=lambda item: item[1][1],reverse=True))
                    found_restaurant=sorted_restaurants[0][0]
                    return render(request,'get_restaurant.html',{"restaurants":found_restaurant,"search": searched_item})
                except:
                    return render(request,'get_restaurant.html',{"search": searched_item})
            except:
                return render(request,'get_restaurant.html',{"search": searched_item})     
        return render(request,'home.html',{"restaurants":data})    
    else:
        return redirect("/login/")