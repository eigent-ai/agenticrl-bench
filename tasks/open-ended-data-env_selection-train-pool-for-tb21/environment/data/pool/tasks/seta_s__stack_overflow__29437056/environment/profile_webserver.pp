class profile::webserver {
  $ssl_cert = lookup('profile::webserver::ssl_cert')
  $ssl_key  = lookup('profile::webserver::ssl_key')

  package { 'apache2':
    ensure => installed,
  }

  file { '/etc/ssl/keys':
    ensure => directory,
    owner  => 'root',
    group  => 'root',
    mode   => '0700',
  }

  file { '/etc/ssl/certs/webapp.crt':
    ensure  => file,
    content => $ssl_cert,
    owner   => 'root',
    group   => 'root',
    mode    => '0644',
    notify  => Service['apache2'],
  }

  file { '/etc/ssl/keys/webapp.key':
    ensure  => file,
    content => $ssl_key,
    owner   => 'root',
    group   => 'root',
    mode    => '0600',
    require => File['/etc/ssl/keys'],
    notify  => Service['apache2'],
  }

  exec { 'enable_ssl_module':
    command => '/usr/sbin/a2enmod ssl',
    creates => '/etc/apache2/mods-enabled/ssl.load',
    require => Package['apache2'],
    notify  => Service['apache2'],
  }

  file { '/etc/apache2/sites-available/webapp.conf':
    ensure  => file,
    content => template('profile/webapp_vhost.conf.erb'),
    require => Package['apache2'],
    notify  => Service['apache2'],
  }

  exec { 'enable_webapp_site':
    command => '/usr/sbin/a2ensite webapp',
    creates => '/etc/apache2/sites-enabled/webapp.conf',
    require => File['/etc/apache2/sites-available/webapp.conf'],
    notify  => Service['apache2'],
  }

  service { 'apache2':
    ensure => running,
  }
}
