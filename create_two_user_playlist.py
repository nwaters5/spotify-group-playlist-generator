import two_user_recommender
import random
rec = two_user_recommender.TwoUserRecommender()

def create(user1, user2):
    user1_playlist, user1_library, user1_profile, user2_playlist, user2_library, user2_profile = rec.get_data(user1, user2)
    rec.initialize(user1_playlist, user1_library, user1_profile, user2_playlist, user2_library, user2_profile)
    rec.fit()
    d1 = rec.get_recommended_playlist()
    rec.initialize(user2_playlist, user2_library, user2_profile, user1_playlist, user1_library, user1_profile)
    rec.fit()
    d2 = rec.get_recommended_playlist()
    res = {**d1, **d2}
    keys = res.keys()
    random.shuffle(keys)
    new_res = {}
    for key in keys:
        new_res.update({key, res[key]})
    return new_res
