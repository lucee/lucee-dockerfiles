VAGRANTFILE_API_VERSION = "2"
WORKBENCH_IP = "192.168.33.200"

Vagrant.require_version ">= 1.7.3"
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  ##################################################
  # Start Docker host
  # - vagrant up dockerhost
  # 
  # Notes
  # - need modern boot2docker image for vagrant; Docker >1.7
  # - https://vagrantcloud.com/dduportal/boxes/boot2docker
  ##################################################
  config.vm.define "dockerhost", autostart: false do |dh|
    dh.vm.box = "dduportal/boot2docker"
    dh.vm.network "private_network", ip: WORKBENCH_IP
    dh.vm.synced_folder ".", "/vagrant", type: "virtualbox"

    # Map Docker VM service ports to VM host
    dh.vm.network :forwarded_port, :host => 8001, :guest => 8001
    dh.vm.network :forwarded_port, :host => 8002, :guest => 8002
    dh.vm.network :forwarded_port, :host => 8003, :guest => 8003
    dh.vm.network :forwarded_port, :host => 8004, :guest => 8004

    dh.vm.provider "virtualbox" do |virtualbox|
      virtualbox.memory = 2048
    end
  end

  ##################################################
  # Launch dev containers
  # - vagrant up lucee45
  # - vagrant up lucee50
  # - vagrant up nginx45
  # - vagrant up nginx50
  ##################################################
  config.vm.define "lucee45", autostart: true do |lucee|
    lucee.vm.provider "docker" do |docker|
      docker.name = "lucee45"
      docker.build_dir = "./4.5"
      # local development code, lucee config & logs
      docker.volumes = [
        "/vagrant/4.5/index.cfm:/var/www/index.cfm"
        ]
      docker.ports = %w(8001:8080)
      docker.vagrant_machine = "dockerhost"
      docker.vagrant_vagrantfile = __FILE__
    end
  end

  config.vm.define "lucee50", autostart: true do |lucee|
    lucee.vm.provider "docker" do |docker|
      docker.name = "lucee50"
      docker.build_dir = "./5.0"
      # local development code, lucee config & logs
      docker.volumes = [
        "/vagrant/5.0/index.cfm:/var/www/index.cfm"
        ]
      docker.ports = %w(8002:8080)
      docker.vagrant_machine = "dockerhost"
      docker.vagrant_vagrantfile = __FILE__
    end
  end

  config.vm.define "nginx45", autostart: true do |lucee|
    lucee.vm.provider "docker" do |docker|
      docker.name = "nginx45"
      docker.build_dir = "./lucee-nginx/4.5"
      # local development code, lucee config & logs
      docker.volumes = [
        "/vagrant/4.5/index.cfm:/var/www/index.cfm"
        ]
      docker.ports = %w(8003:80)
      docker.vagrant_machine = "dockerhost"
      docker.vagrant_vagrantfile = __FILE__
    end
  end

  config.vm.define "nginx50", autostart: true do |lucee|
    lucee.vm.provider "docker" do |docker|
      docker.name = "nginx50"
      docker.build_dir = "./lucee-nginx/5.0"
      # local development code, lucee config & logs
      docker.volumes = [
        "/vagrant/5.0/index.cfm:/var/www/index.cfm"
        ]
      docker.ports = %w(8004:80)
      docker.vagrant_machine = "dockerhost"
      docker.vagrant_vagrantfile = __FILE__
    end
  end

  ##################################################
  # Handy config locations...
  # docker.volumes = [
  #   "/vagrant/4.5/index.cfm:/var/www/index.cfm",
  #   "/vagrant/config/lucee/local-lucee-server.xml:/opt/lucee/server/lucee-server/context/lucee-server.xml",
  #   "/vagrant/config/lucee/local-lucee-web.xml.cfm:/opt/lucee/web/lucee-web.xml.cfm",
  #   "/vagrant/logs/lucee:/opt/lucee/web/logs",
  #   "/vagrant/logs/nginx:/var/log/nginx",
  #   "/vagrant/logs/supervisor:/var/log/supervisor",
  #   "/vagrant/logs/tomcat:/usr/local/tomcat/logs"
  #   ]
  ##################################################

# /config
end