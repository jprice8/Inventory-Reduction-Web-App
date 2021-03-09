from django.core.mail import send_mail, EmailMessage
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count
from django.contrib.auth.models import User

from target.models import MovementPlan

class Command(BaseCommand):
    help = 'Sending an email with django'

    def handle(self, *args, **options):
        # test emails
        TEST1 = 'jdprice1995@gmail.com'
        TEST2 = 'jdprice@baptisthealthsystem.com'

        # dmm emails
        EMAIL939 = 'jdveale@baptisthealthsystem.com'
        EMAIL971 = 'crdas@baptisthealthsystem.com'
        EMAIL952 = 'sxanders4@baptisthealthsystem.com'
        EMAIL872 = 'mamoelle@resolutehealth.com'
        EMAIL968 = 'mxvillal@baptisthealthsystem.com'
        EMAIL954 = 'axbradfo@baptisthealthsystem.com'

        def sendWeeklyEmail(dmm_email, dmm_fac, num_plans):
            # send email
            mySubject = "Movement Plans Awaiting Your Decision"
            myBody = "Hello DMM at Facility " + dmm_fac + ", \n" \
                " \n" \
                "You have " + str(num_plans) + " outstanding request(s) awaiting your decision. \n" \
                " \n" \
                "Please go to reductiontoolkit.com to either accept or reject them."

            mySender = 'noreply@reductiontoolkit.com'
            send_mail(
                mySubject,
                myBody,
                mySender,
                [dmm_email],
            )

        try:
            plans = MovementPlan.objects.filter(
                isFinalized=False
            ).exclude(
                ship_fac='TEN'
            ).exclude(
                ship_fac='NON'
            ).values(
                'ship_fac'
            ).annotate(
                outstanding_plans=Count('id')
            )

            for plan in plans:
                shipFac = plan['ship_fac']
                planQty = plan['outstanding_plans']

                # send email function
                if shipFac == '939':
                    sendWeeklyEmail(EMAIL939, shipFac, planQty)
                elif shipFac == '971':
                    sendWeeklyEmail(EMAIL971, shipFac, planQty)
                elif shipFac == '952':
                    sendWeeklyEmail(EMAIL952, shipFac, planQty)
                elif shipFac == '872':
                    sendWeeklyEmail(EMAIL872, shipFac, planQty)
                elif shipFac == '968':
                    sendWeeklyEmail(EMAIL968, shipFac, planQty)
                elif shipFac == '954':
                    sendWeeklyEmail(EMAIL954, shipFac, planQty)
                else:
                    self.stdout.write(self.style.WARNING('Check if/else code. Facility leakage.'))
                
        except MovementPlan.DoesNotExist:
            raise CommandError('Could not find movement plans')