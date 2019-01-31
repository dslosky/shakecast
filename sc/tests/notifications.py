import sys
import unittest

from sc.app.notifications import *
from sc.app.orm import dbconnect, Facility, FacilityShaking, Group, Notification
from util import create_group

class TestMailer(unittest.TestCase):
    '''
    Test the connection to the SMTP server
    '''
    def test_initMailer(self):
        '''
        Fails when the Mailer is unable to initialize. Failure
        is caused by code errors or proxy access
        '''
        m = Mailer()
    
    def test_sendMail(self):
        '''
        Send an email with Mailer object. Will fail with code errors or
        failure to reach SMTP server
        '''
        m = Mailer()
        
        you = self.email
        msg = MIMEText('This email is a test of your ShakeCast SMTP server')
        msg['Subject'] = 'ShakeCast SMTP TEST'
        msg['From'] = m.me
        msg['To'] = you
        
        m.send(msg=msg, you=you)

class TestGroupGetsNotification(unittest.TestCase):

    @dbconnect
    def test_forFirstNotification(self, session=None):

        sm1 = ShakeMap(
            shakemap_id = 'shakemap1',
            shakemap_version = 1
        )

        session.add(sm1)

        group = create_group(name='GLOBAL')

        session.add(group)

        n1 = Notification(
            shakemap = sm1
        )

        session.add(n1)

        session.commit()

        # check notification 1
        has_alert_level, new_inspection, update = check_notification_for_group(
                                                    group,
                                                    n1,
                                                    session=session
                                                )
        self.assertTrue(has_alert_level)
        self.assertTrue(new_inspection)
        self.assertFalse(update)

        objs = [sm1, group ,n1]
        for obj in objs:
            session.delete(obj)

        session.commit()

    @dbconnect
    def test_updateNotificationNoneNone(self, session=None):

        sm1 = ShakeMap(
            shakemap_id = 'shakemap1',
            shakemap_version = 1
        )

        sm2 = ShakeMap(
            shakemap_id = 'shakemap1',
            shakemap_version = 2
        )

        session.add_all([sm1, sm2])

        group = create_group(name='GLOBAL')

        session.add(group)

        n1 = Notification(
            shakemap = sm1
        )

        n2 = Notification(
            shakemap = sm2
        )

        session.add_all([n1, n2])

        session.commit()

        # check notification 1
        has_alert_level, new_inspection, update = check_notification_for_group(
                                                    group,
                                                    n2,
                                                    session=session
                                                )
        self.assertTrue(has_alert_level)
        self.assertFalse(new_inspection)
        self.assertTrue(update)

        objs = [sm1, sm2, n1, n2, group]
        for obj in objs:
            session.delete(obj)
        
        session.commit()

    @dbconnect
    def test_changedNotificationNoneGrey(self, session=None):

        sm1 = ShakeMap(
            shakemap_id = 'shakemap1',
            shakemap_version = 1
        )

        sm2 = ShakeMap(
            shakemap_id = 'shakemap1',
            shakemap_version = 2
        )

        session.add_all([sm1, sm2])

        group = create_group(name='GLOBAL')

        session.add(group)

        n1 = Notification(
            shakemap = sm1
        )

        n2 = Notification(
            shakemap = sm2
        )

        session.add_all([n1, n2])

        fs = FacilityShaking(
            shakemap = sm2,
            weight = .5
        )

        session.add(fs)

        session.commit()

        # check notification 1
        has_alert_level, new_inspection, update = check_notification_for_group(
                                                    group,
                                                    n2,
                                                    session=session
                                                )
        self.assertTrue(has_alert_level)
        self.assertTrue(new_inspection)
        self.assertTrue(update)

        objs = [sm1, sm2, n1, n2, group]
        for obj in objs:
            session.delete(obj)
        
        session.commit()

    @dbconnect
    def test_changedNotificationGreyGreen(self, session=None):

        sm1 = ShakeMap(
            shakemap_id = 'shakemap1',
            shakemap_version = 1
        )

        sm2 = ShakeMap(
            shakemap_id = 'shakemap1',
            shakemap_version = 2
        )

        session.add_all([sm1, sm2])

        group = create_group(name='GLOBAL')

        session.add(group)

        n1 = Notification(
            shakemap = sm1
        )

        n2 = Notification(
            shakemap = sm2
        )

        session.add_all([n1, n2])

        fs1 = FacilityShaking(
            shakemap = sm1,
            weight = .1
        )

        fs2 = FacilityShaking(
            shakemap = sm2,
            weight = 1
        )

        session.add_all([fs1, fs2])

        session.commit()

        # check notification 1
        has_alert_level, new_inspection, update = check_notification_for_group(
                                                    group,
                                                    n2,
                                                    session=session
                                                )
        self.assertTrue(has_alert_level)
        self.assertTrue(new_inspection)
        self.assertTrue(update)

        objs = [sm1, sm2, n1, n2, group]
        for obj in objs:
            session.delete(obj)
        
        session.commit()

    @dbconnect
    def test_unchangedNotificationGreenGreen(self, session=None):
        sm1 = ShakeMap(
            shakemap_id = 'shakemap1',
            shakemap_version = 1
        )

        sm2 = ShakeMap(
            shakemap_id = 'shakemap1',
            shakemap_version = 2
        )

        session.add_all([sm1, sm2])

        group = create_group(name='GLOBAL')

        session.add(group)

        n1 = Notification(
            shakemap = sm1
        )

        n2 = Notification(
            shakemap = sm2
        )

        session.add_all([n1, n2])

        fac1 = Facility(
            facility_id = 1
        )

        fs1 = FacilityShaking(
            shakemap = sm1,
            weight = 1,
            facility = fac1
        )

        fs2 = FacilityShaking(
            shakemap = sm2,
            weight = 1,
            facility = fac1
        )

        session.add_all([fac1, fs1, fs2])

        session.commit()

        # check notification 1
        has_alert_level, new_inspection, update = check_notification_for_group(
                                                    group,
                                                    n2,
                                                    session=session
                                                )
        self.assertTrue(has_alert_level)
        self.assertFalse(new_inspection)
        self.assertTrue(update)

        objs = [sm1, sm2, n1, n2, group, fac1]
        for obj in objs:
            session.delete(obj)
        
        session.commit()

    @dbconnect
    def test_changedNotificationGreenGreen(self, session=None):
        sm1 = ShakeMap(
            shakemap_id = 'shakemap1',
            shakemap_version = 1
        )

        sm2 = ShakeMap(
            shakemap_id = 'shakemap1',
            shakemap_version = 2
        )

        session.add_all([sm1, sm2])

        group = create_group(name='GLOBAL')

        session.add(group)

        n1 = Notification(
            shakemap = sm1
        )

        n2 = Notification(
            shakemap = sm2
        )

        session.add_all([n1, n2])

        fac1 = Facility(
            facility_id = 1
        )

        fac2 = Facility(
            facility_id = 2
        )

        fs1 = FacilityShaking(
            shakemap = sm1,
            weight = 1,
            facility = fac1
        )

        fs2 = FacilityShaking(
            shakemap = sm2,
            weight = 1,
            facility = fac2
        )

        session.add_all([fac1, fs1, fs2])

        session.commit()

        # check notification 1
        has_alert_level, new_inspection, update = check_notification_for_group(
                                                    group,
                                                    n2,
                                                    session=session
                                                )
        self.assertTrue(has_alert_level)
        self.assertTrue(new_inspection)
        self.assertTrue(update)

        objs = [sm1, sm2, n1, n2, group, fac1, fac2]
        for obj in objs:
            session.delete(obj)
        
        session.commit()

    @dbconnect
    def test_changedNotificationLength(self, session=None):
        sm1 = ShakeMap(
            shakemap_id = 'shakemap1',
            shakemap_version = 1
        )

        sm2 = ShakeMap(
            shakemap_id = 'shakemap1',
            shakemap_version = 2
        )

        session.add_all([sm1, sm2])

        group = create_group(name='GLOBAL')

        session.add(group)

        n1 = Notification(
            shakemap = sm1
        )

        n2 = Notification(
            shakemap = sm2
        )

        session.add_all([n1, n2])

        fac1 = Facility(
            facility_id = 1
        )

        fac2 = Facility(
            facility_id = 2
        )

        fac3 = Facility(
            facility_id = 3
        )

        fs1 = FacilityShaking(
            shakemap = sm1,
            weight = 1,
            facility = fac1
        )

        fs2 = FacilityShaking(
            shakemap = sm2,
            weight = 1,
            facility = fac2
        )

        fs3 = FacilityShaking(
            shakemap = sm2,
            weight = .1,
            facility = fac3
        )

        session.add_all([fac1, fac2, fac3, fs1, fs2, fs3])

        session.commit()

        # check notification 1
        has_alert_level, new_inspection, update = check_notification_for_group(
                                                    group,
                                                    n2,
                                                    session=session
                                                )
        self.assertTrue(has_alert_level)
        self.assertTrue(new_inspection)
        self.assertTrue(update)

        objs = [sm1, sm2, n1, n2, group, fac1, fac2, fac3]
        for obj in objs:
            session.delete(obj)
        
        session.commit()


class TestTemplateManager(unittest.TestCase):
    '''
    Test the ShakeCast notification configuration. Fails if code errors
    '''

    def test_notificationConfigs(self):
        temp_manager = TemplateManager()
        configs = temp_manager.get_configs('new_event', 'default')
        self.assertIsNotNone(configs)
        configs = temp_manager.save_configs('new_event', 'default', configs)
        self.assertIsNotNone(configs)
    
    def test_badNotificationConfigs(self):
        temp_manager = TemplateManager()
        bad_configs = temp_manager.get_configs('new_event', 'template_DOES_NOT_EXIST_!@#$')
        default = temp_manager.get_configs('new_event', 'default')

        self.assertEqual(bad_configs, default)

        bad_configs = temp_manager.save_configs('new_event', 'template_DOES_NOT_EXIST_!@#$', None)
        self.assertIsNone(bad_configs)

    def test_getTemplate(self):
        temp_manager = TemplateManager()
        temp = temp_manager.get_template('new_event', 'default')
        self.assertIsNotNone(temp)

    def test_badTemplate(self):
        temp_manager = TemplateManager()
        temp = temp_manager.get_template('new_event', 'template_DOES_NOT_EXIST_!@#$')
        self.assertIsNotNone(temp)

        temp = temp_manager.get_template_string('new_event', 'template_DOES_NOT_EXIST_!@#$')
        self.assertIsNone(temp)

    def test_templateNames(self):
        temp_manager = TemplateManager()
        temp_names = temp_manager.get_template_names()
        self.assertIn('default', temp_names)

    def test_NewTemp(self):
        temp_manager = TemplateManager()
        result = temp_manager.create_new('default')

        self.assertTrue(result)
    
    def test_pdfTemplate(self):
        temp_manager = TemplateManager()
        result = temp_manager.get_template('pdf', 'header', sub_dir='default')
    
    def test_badSubdirPdfTemplate(self):
        temp_manager = TemplateManager()
        result = temp_manager.get_template('pdf', 'header', sub_dir='BAAAADSUBDIR')

def set_email():
    # If the user wants to make sure they can get emails, they should
    # be able to specify an email address for each test run
    if len(sys.argv) > 1:
        email = sys.argv[1]
        del sys.argv[1]
        if (('@' in email) and
                ('.' in email) and
                ('com' in email or
                 'gov' in email or
                 'org' in email or
                 'edu' in email)):
            unittest.TestCase.email = email
    else:
        unittest.TestCase.email = 'test@test.com'

if __name__ == '__main__':
    set_email()
    unittest.main()