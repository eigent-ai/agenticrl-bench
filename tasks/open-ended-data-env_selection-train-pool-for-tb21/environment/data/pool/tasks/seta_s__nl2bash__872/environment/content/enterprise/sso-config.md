# Single Sign-On Configuration

Configure SAML 2.0 or OpenID Connect (OIDC) for enterprise single sign-on integration with your identity provider.

## SAML 2.0 Setup

To configure SAML, you need the Identity Provider metadata XML, the entity ID, and the assertion consumer service URL. Upload the metadata through the admin panel under Security > SSO.

## OIDC Setup

For OpenID Connect, provide the client ID, client secret, and discovery URL from your identity provider. The platform supports authorization code flow with PKCE.

## Group Mapping

Map identity provider groups to platform roles for automated access control. Group names are case-sensitive and must match exactly.
