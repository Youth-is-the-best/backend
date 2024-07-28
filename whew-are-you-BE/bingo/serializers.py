from rest_framework import serializers
from .models import Bingo, BingoSpace, CustomBingoItem, ProvidedBingoItem, ToDo
from review_information.models import ReviewImage, Review
from rest_framework import status
from rest_framework.response import Response

class BingoSpaceSerializer(serializers.ModelSerializer):
    class Meta: 
        model = BingoSpace
        fields = "__all__"

class CustomBingoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomBingoItem
        fields = "__all__"

class ProvidedBingoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProvidedBingoItem
        fields = "__all__"

class ToDoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDo
        fields = "__all__"


# 후기글 작성 시리얼라이저
class ReviewPOSTSerializer(serializers.ModelSerializer):
    location = serializers.CharField()

    class Meta:
        model = Review
        fields = ["location", "procedure", "content", "large_category"]

    def create(self, validated_data):
        large_category = validated_data['large_category']
        location = int(validated_data['location'])
        procedure = validated_data['procedure']
        content = validated_data['content']
        images = self.context['request'].FILES.getlist('images')
        user = self.context['user'].user
        bingo = Bingo.objects.get(user=user, is_activate=True)
        bingo_space = BingoSpace.objects.get(bingo=bingo, location=location)
        todo = bingo_space.todo.all()
        date = bingo_space.date     # 시험 날짜
        start_date_user = bingo_space.start_date
        end_date_user = bingo_space.end_date

        # 끌어오기 항목의 후기글인 경우
        if bingo_space.recommend_content:
            title = bingo_space.recommend_content.title
            duty = bingo_space.recommend_content.duty
            employment_form = bingo_space.recommend_content.employment_form
            area = bingo_space.recommend_content.area
            start_date = bingo_space.recommend_content.start_date
            end_date = bingo_space.recommend_content.end_date
            host = bingo_space.recommend_content.host
            app_fee = bingo_space.recommend_content.app_fee
            prep_period = bingo_space.recommend_content.prep_period
            app_due = bingo_space.recommend_content.app_due
            field = bingo_space.recommend_content.field

        # 직접 작성한 항목의 후기글인 경우
        elif bingo_space.self_content:
            title = bingo_space.self_content.title
            duty = bingo_space.self_content.duty
            employment_form = bingo_space.self_content.employment_form
            area = bingo_space.self_content.area
            start_date = bingo_space.self_content.start_date
            end_date = bingo_space.self_content.end_date
            host = bingo_space.self_content.host
            app_fee = bingo_space.self_content.app_fee
            prep_period = bingo_space.self_content.prep_period
            app_due = bingo_space.self_content.app_due
            field = bingo_space.self_content.field

        # 인턴(채용) 카테고리인 경우
        if large_category == 'CAREER':
            review = Review(user=user, title=title, large_category=large_category, duty=duty, employment_form=employment_form, area=area, start_date=start_date, end_date=end_date, bingo_space=bingo_space, content=content, todo=todo, procedure=procedure)
        # 자격증 카테고리인 경우
        elif large_category == 'CERTIFICATE':
            review = Review(user=user, bingo_space=bingo_space, title=title, large_category=large_category, host=host, app_fee=app_fee, date=date, start_date=start_date_user, end_date=end_date_user, todo=todo, procedure=procedure, content=content)
        # 대외 활동 카테고리인 경우
        elif large_category == 'OUTBOUND':
            review = Review(user=user, bingo_space=bingo_space, title=title, large_category=large_category, start_date=start_date_user, end_date=end_date_user, field=field, area=area, todo=todo, procedure=procedure, content=content)
        # 공모전 카테고리인 경우
        elif large_category == 'CONTEST':
            review = Review(user=user, bingo_space=bingo_space, title=title, large_category=large_category, host=host, field=field, date=date, start_date=start_date_user, end_date=end_date_user, todo=todo, procedure=procedure, content=content)
        # 그 외(취미, 여행, 자기 계발, 휴식)
        elif large_category in ['HOBBY', 'TRAVEL', 'SELFIMPROVEMENT', 'REST']:
            review = Review(bingo_space=bingo_space, title=title, large_category=large_category, start_date=start_date, end_date=end_date, todo=todo, content=content)
        # 잘못 입력
        else:
            return Response({"error": "요청한 카테고리 항목이 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        review.save()
        bingo_space.is_executed = True      # 빙고 완료 표시
        bingo_space.save()

        for image in images:
            image_data = ReviewImage(review=review, image=image)
            image_data.save()
        validated_data['images'] = images
        return validated_data