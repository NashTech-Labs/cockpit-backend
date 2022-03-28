# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class GuacamoleConnection(models.Model):
    connection_id = models.AutoField(primary_key=True)
    connection_name = models.CharField(max_length=128)
    parent = models.ForeignKey('GuacamoleConnectionGroup', models.DO_NOTHING, blank=True, null=True)
    protocol = models.CharField(max_length=32)
    max_connections = models.IntegerField(blank=True, null=True)
    max_connections_per_user = models.IntegerField(blank=True, null=True)
    connection_weight = models.IntegerField(blank=True, null=True)
    failover_only = models.BooleanField()
    proxy_port = models.IntegerField(blank=True, null=True)
    proxy_hostname = models.CharField(max_length=512, blank=True, null=True)
    proxy_encryption_method = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'guacamole_connection'
        unique_together = (('connection_name', 'parent'),)


class GuacamoleConnectionAttribute(models.Model):
    connection = models.OneToOneField(GuacamoleConnection, models.DO_NOTHING, primary_key=True)
    attribute_name = models.CharField(max_length=128)
    attribute_value = models.CharField(max_length=4096)

    class Meta:
        managed = False
        db_table = 'guacamole_connection_attribute'
        unique_together = (('connection', 'attribute_name'),)


class GuacamoleConnectionGroup(models.Model):
    connection_group_id = models.AutoField(primary_key=True)
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    connection_group_name = models.CharField(max_length=128)
    type = models.TextField()  # This field type is a guess.
    max_connections = models.IntegerField(blank=True, null=True)
    max_connections_per_user = models.IntegerField(blank=True, null=True)
    enable_session_affinity = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'guacamole_connection_group'
        unique_together = (('connection_group_name', 'parent'),)


class GuacamoleConnectionGroupAttribute(models.Model):
    connection_group = models.OneToOneField(GuacamoleConnectionGroup, models.DO_NOTHING, primary_key=True)
    attribute_name = models.CharField(max_length=128)
    attribute_value = models.CharField(max_length=4096)

    class Meta:
        managed = False
        db_table = 'guacamole_connection_group_attribute'
        unique_together = (('connection_group', 'attribute_name'),)


class GuacamoleConnectionGroupPermission(models.Model):
    entity = models.OneToOneField('GuacamoleEntity', models.DO_NOTHING, primary_key=True)
    connection_group = models.ForeignKey(GuacamoleConnectionGroup, models.DO_NOTHING)
    permission = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'guacamole_connection_group_permission'
        unique_together = (('entity', 'connection_group', 'permission'),)


class GuacamoleConnectionHistory(models.Model):
    history_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('GuacamoleUser', models.DO_NOTHING, blank=True, null=True)
    username = models.CharField(max_length=128)
    remote_host = models.CharField(max_length=256, blank=True, null=True)
    connection = models.ForeignKey(GuacamoleConnection, models.DO_NOTHING, blank=True, null=True)
    connection_name = models.CharField(max_length=128)
    sharing_profile = models.ForeignKey('GuacamoleSharingProfile', models.DO_NOTHING, blank=True, null=True)
    sharing_profile_name = models.CharField(max_length=128, blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'guacamole_connection_history'


class GuacamoleConnectionParameter(models.Model):
    connection = models.OneToOneField(GuacamoleConnection, models.DO_NOTHING, primary_key=True)
    parameter_name = models.CharField(max_length=128)
    parameter_value = models.CharField(max_length=4096)

    class Meta:
        managed = False
        db_table = 'guacamole_connection_parameter'
        unique_together = (('connection', 'parameter_name'),)


class GuacamoleConnectionPermission(models.Model):
    entity = models.OneToOneField('GuacamoleEntity', models.DO_NOTHING, primary_key=True)
    connection = models.ForeignKey(GuacamoleConnection, models.DO_NOTHING)
    permission = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'guacamole_connection_permission'
        unique_together = (('entity', 'connection', 'permission'),)


class GuacamoleEntity(models.Model):
    entity_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    type = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'guacamole_entity'
        unique_together = (('type', 'name'),)


class GuacamoleSharingProfile(models.Model):
    sharing_profile_id = models.AutoField(primary_key=True)
    sharing_profile_name = models.CharField(max_length=128)
    primary_connection = models.ForeignKey(GuacamoleConnection, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'guacamole_sharing_profile'
        unique_together = (('sharing_profile_name', 'primary_connection'),)


class GuacamoleSharingProfileAttribute(models.Model):
    sharing_profile = models.OneToOneField(GuacamoleSharingProfile, models.DO_NOTHING, primary_key=True)
    attribute_name = models.CharField(max_length=128)
    attribute_value = models.CharField(max_length=4096)

    class Meta:
        managed = False
        db_table = 'guacamole_sharing_profile_attribute'
        unique_together = (('sharing_profile', 'attribute_name'),)


class GuacamoleSharingProfileParameter(models.Model):
    sharing_profile = models.OneToOneField(GuacamoleSharingProfile, models.DO_NOTHING, primary_key=True)
    parameter_name = models.CharField(max_length=128)
    parameter_value = models.CharField(max_length=4096)

    class Meta:
        managed = False
        db_table = 'guacamole_sharing_profile_parameter'
        unique_together = (('sharing_profile', 'parameter_name'),)


class GuacamoleSharingProfilePermission(models.Model):
    entity = models.OneToOneField(GuacamoleEntity, models.DO_NOTHING, primary_key=True)
    sharing_profile = models.ForeignKey(GuacamoleSharingProfile, models.DO_NOTHING)
    permission = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'guacamole_sharing_profile_permission'
        unique_together = (('entity', 'sharing_profile', 'permission'),)


class GuacamoleSystemPermission(models.Model):
    entity = models.OneToOneField(GuacamoleEntity, models.DO_NOTHING, primary_key=True)
    permission = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'guacamole_system_permission'
        unique_together = (('entity', 'permission'),)


class GuacamoleUser(models.Model):
    user_id = models.AutoField(primary_key=True)
    entity = models.OneToOneField(GuacamoleEntity, models.DO_NOTHING)
    password_hash = models.BinaryField()
    password_salt = models.BinaryField(blank=True, null=True)
    password_date = models.DateTimeField()
    disabled = models.BooleanField()
    expired = models.BooleanField()
    access_window_start = models.TimeField(blank=True, null=True)
    access_window_end = models.TimeField(blank=True, null=True)
    valid_from = models.DateField(blank=True, null=True)
    valid_until = models.DateField(blank=True, null=True)
    timezone = models.CharField(max_length=64, blank=True, null=True)
    full_name = models.CharField(max_length=256, blank=True, null=True)
    email_address = models.CharField(max_length=256, blank=True, null=True)
    organization = models.CharField(max_length=256, blank=True, null=True)
    organizational_role = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'guacamole_user'


class GuacamoleUserAttribute(models.Model):
    user = models.OneToOneField(GuacamoleUser, models.DO_NOTHING, primary_key=True)
    attribute_name = models.CharField(max_length=128)
    attribute_value = models.CharField(max_length=4096)

    class Meta:
        managed = False
        db_table = 'guacamole_user_attribute'
        unique_together = (('user', 'attribute_name'),)


class GuacamoleUserGroup(models.Model):
    user_group_id = models.AutoField(primary_key=True)
    entity = models.OneToOneField(GuacamoleEntity, models.DO_NOTHING)
    disabled = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'guacamole_user_group'


class GuacamoleUserGroupAttribute(models.Model):
    user_group = models.OneToOneField(GuacamoleUserGroup, models.DO_NOTHING, primary_key=True)
    attribute_name = models.CharField(max_length=128)
    attribute_value = models.CharField(max_length=4096)

    class Meta:
        managed = False
        db_table = 'guacamole_user_group_attribute'
        unique_together = (('user_group', 'attribute_name'),)


class GuacamoleUserGroupMember(models.Model):
    user_group = models.OneToOneField(GuacamoleUserGroup, models.DO_NOTHING, primary_key=True)
    member_entity = models.ForeignKey(GuacamoleEntity, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'guacamole_user_group_member'
        unique_together = (('user_group', 'member_entity'),)


class GuacamoleUserGroupPermission(models.Model):
    entity = models.OneToOneField(GuacamoleEntity, models.DO_NOTHING, primary_key=True)
    affected_user_group = models.ForeignKey(GuacamoleUserGroup, models.DO_NOTHING)
    permission = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'guacamole_user_group_permission'
        unique_together = (('entity', 'affected_user_group', 'permission'),)


class GuacamoleUserHistory(models.Model):
    history_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(GuacamoleUser, models.DO_NOTHING, blank=True, null=True)
    username = models.CharField(max_length=128)
    remote_host = models.CharField(max_length=256, blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'guacamole_user_history'


class GuacamoleUserPasswordHistory(models.Model):
    password_history_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(GuacamoleUser, models.DO_NOTHING)
    password_hash = models.BinaryField()
    password_salt = models.BinaryField(blank=True, null=True)
    password_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'guacamole_user_password_history'


class GuacamoleUserPermission(models.Model):
    entity = models.OneToOneField(GuacamoleEntity, models.DO_NOTHING, primary_key=True)
    affected_user = models.ForeignKey(GuacamoleUser, models.DO_NOTHING)
    permission = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'guacamole_user_permission'
        unique_together = (('entity', 'affected_user', 'permission'),)
