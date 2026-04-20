CookieConsent.run({
  categories: {
    necessary: {
      enabled: true,
      readOnly: true
    },
    analytics: {}
  },

  language: {
    default: 'en',
    translations: {
      en: {
        consentModal: {
          title: 'We use cookies',
          description: 'We use analytics cookies to understand how visitors use our site. You can choose to accept or decline.',
          acceptAllBtn: 'Accept all',
          rejectAllBtn: 'Reject all',
          showPreferencesBtn: 'Manage preferences'
        },
        preferencesModal: {
          title: 'Cookie preferences',
          acceptAllBtn: 'Accept all',
          rejectAllBtn: 'Reject all',
          savePreferencesBtn: 'Save preferences',
          sections: [
            {
              title: 'Strictly necessary',
              description: 'These cookies are required for the site to work.',
              linkedCategory: 'necessary'
            },
            {
              title: 'Analytics',
              description: 'Help us understand how visitors use our site.',
              linkedCategory: 'analytics'
            }
          ]
        }
      }
    }
  },

  onConsent: function() {
    if (CookieConsent.acceptedCategory('analytics')) {
      gtag('consent', 'update', { 'analytics_storage': 'granted' });
    }
  },

  onChange: function() {
    if (CookieConsent.acceptedCategory('analytics')) {
      gtag('consent', 'update', { 'analytics_storage': 'granted' });
    } else {
      gtag('consent', 'update', { 'analytics_storage': 'denied' });
    }
  }
});