class UserOutputAdapter():

    def parse(self, user):
        return {
            'name': user.name,
            'surname':user.surname,
            'email': user.email,
            'mobile': user.mobile,
            'username': user.username,
            'password': user.password,
            'company_name': user.company_name,
            'designation': user.designation,
            'facebook': user.facebook,
            'twitter': user.twitter,
            'linkedin': user.linkedin,
            'instagram': user.instagram,
            'address': user.address,
            'city': user.city,
            'state': user.state,
            'country': user.country,
            'profile': user.profile_picture

        }
