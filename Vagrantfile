##################################################
# Workbench Settings
##################################################
Vagrant.require_version ">= 1.7.3"

PROJECT_ENV = File.basename(Dir.getwd)

if File.exist?('../Vagrantfile')
  WORKBENCH_HOST = "workbench"
  WORKBENCH_VAGRANTFILE = "../Vagrantfile"
else
  WORKBENCH_HOST = "dockerhost"
  WORKBENCH_VAGRANTFILE = __FILE__
end

Vagrant.configure("2") do |config|

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
      docker.env = {
        VIRTUAL_HOST: "lucee45.*"
      }
      # local development code, lucee config & logs
      docker.volumes = [
        "/vagrant/" + PROJECT_ENV + "/4.5/index.cfm:/var/www/index.cfm"
        ]
      docker.ports = %w(8001:8080)
      docker.vagrant_machine = WORKBENCH_HOST
      docker.vagrant_vagrantfile = WORKBENCH_VAGRANTFILE
      docker.force_host_vm = true
    end
    puts '############################################################'
    puts '# LUCEE45'
    puts '#  - workbench at: http://workbench:8001'
    puts '#  - stand-alone at: http://192.168.56.100:8001'
    puts '############################################################'
  end

  config.vm.define "lucee50", autostart: true do |lucee|
    lucee.vm.provider "docker" do |docker|
      docker.name = "lucee50"
      docker.build_dir = "./5.0"
      docker.env = {
        VIRTUAL_HOST: "lucee50.*"
      }
      # local development code, lucee config & logs
      docker.volumes = [
        "/vagrant/" + PROJECT_ENV + "/5.0/index.cfm:/var/www/index.cfm"
        ]
      docker.ports = %w(8002:8080)
      docker.vagrant_machine = WORKBENCH_HOST
      docker.vagrant_vagrantfile = WORKBENCH_VAGRANTFILE
      docker.force_host_vm = true
    end
    puts '############################################################'
    puts '# LUCEE50'
    puts '#  - workbench at: http://workbench:8002'
    puts '#  - stand-alone at: http://192.168.56.100:8002'
    puts '############################################################'
  end

  config.vm.define "nginx45", autostart: true do |lucee|
    lucee.vm.provider "docker" do |docker|
      docker.name = "nginx45"
      docker.build_dir = "./lucee-nginx/4.5"
      docker.env = {
        VIRTUAL_HOST: "nginx45.*"
      }
      # local development code, lucee config & logs
      docker.volumes = [
        "/vagrant/" + PROJECT_ENV + "/4.5/index.cfm:/var/www/index.cfm"
        ]
      docker.ports = %w(8003:80)
      docker.vagrant_machine = WORKBENCH_HOST
      docker.vagrant_vagrantfile = WORKBENCH_VAGRANTFILE
      docker.force_host_vm = true
    end
    puts '############################################################'
    puts '# NGINX45'
    puts '#  - workbench at: http://nginx45.dev'
    puts '#  - stand-alone at: http://192.168.56.100:8003'
    puts '############################################################'
  end

  config.vm.define "nginx50", autostart: true do |lucee|
    lucee.vm.provider "docker" do |docker|
      docker.name = "nginx50"
      docker.build_dir = "./lucee-nginx/5.0"
      docker.env = {
        VIRTUAL_HOST: "nginx50.*"
      }
      # local development code, lucee config & logs
      docker.volumes = [
        "/vagrant/" + PROJECT_ENV + "/5.0/index.cfm:/var/www/index.cfm"
        ]
      docker.ports = %w(8004:80)
      docker.vagrant_machine = WORKBENCH_HOST
      docker.vagrant_vagrantfile = WORKBENCH_VAGRANTFILE
      docker.force_host_vm = true
    end
    puts '############################################################'
    puts '# NGINX50'
    puts '#  - workbench at: http://nginx50.dev'
    puts '#  - stand-alone at: http://192.168.56.100:8004'
    puts '############################################################'
  end


  ##################################################
  # Solo Docker Host; 
  #   fallback for missing parent boot2docker env
  ##################################################
  config.vm.define "dockerhost", autostart: false do |dh|
    dh.vm.box = "dduportal/boot2docker"
    dh.vm.network "private_network", ip: "192.168.56.100"
    dh.vm.synced_folder ".", "/vagrant/" + PROJECT_ENV, type: "virtualbox"

    dh.vm.provider "virtualbox" do |vb|
      vb.memory = 2048
      vb.customize ["modifyvm", :id, "--nictype2", "virtio"]
    end

    puts '############################################################'
    puts '#  SOLO-DOCKERHOST... http://192.168.56.100'
    puts '# '
    puts '#  Backup for missing Workbench Boot2Docker. Consider'
    puts '#  setting up the complete development environment:'
    puts '#    https://github.com/Daemonite/workbench'
    puts '############################################################'
  end

# /config
end

##################################################
# Handy additional config locations...
# local development code, lucee config & logs
# docker.volumes = [
#   "/vagrant/" + PROJECT_ENV + "/code:/var/www/farcry",
#   "/vagrant/" + PROJECT_ENV + "/config/lucee/lucee-web.xml.cfm:/opt/lucee/web/lucee-web.xml.cfm",
#   "/vagrant/" + PROJECT_ENV + "/logs/lucee:/opt/lucee/web/logs",
#   "/vagrant/" + PROJECT_ENV + "/logs/nginx:/var/log/nginx",
#   "/vagrant/" + PROJECT_ENV + "/logs/supervisor:/var/log/supervisor",
#   "/vagrant/" + PROJECT_ENV + "/logs/tomcat:/usr/local/tomcat/logs"
#   ]
##################################################
