from django.conf import settings
from django.test.runner import DiscoverRunner


class AppsTestSuiteRunner(DiscoverRunner):

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        if not test_labels:
            # Only test our apps
            test_labels = settings.COMMON_APPS
            print ('Testing: ' + str(test_labels))

        return super(AppsTestSuiteRunner, self).run_tests(
                test_labels, extra_tests, **kwargs)
