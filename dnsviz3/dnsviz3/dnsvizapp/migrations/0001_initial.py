# Generated by Django 3.2.7 on 2021-09-13 13:20

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import dnsviz.analysis.offline
import dnsvizapp.fields
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DNSQuery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qname', dnsvizapp.fields.DomainNameField(max_length=2048)),
                ('rdtype', dnsvizapp.fields.UnsignedSmallIntegerField()),
                ('rdclass', dnsvizapp.fields.UnsignedSmallIntegerField()),
                ('response_options', dnsvizapp.fields.UnsignedSmallIntegerField(default=0)),
                ('version', models.PositiveSmallIntegerField(default=3)),
            ],
        ),
        migrations.CreateModel(
            name='DNSResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server', models.GenericIPAddressField()),
                ('client', models.GenericIPAddressField()),
                ('flags', dnsvizapp.fields.UnsignedSmallIntegerField(blank=True, null=True)),
                ('has_question', models.BooleanField(default=True)),
                ('question_name', dnsvizapp.fields.DomainNameField(blank=True, max_length=2048, null=True)),
                ('question_rdtype', dnsvizapp.fields.UnsignedSmallIntegerField(blank=True, null=True)),
                ('question_rdclass', dnsvizapp.fields.UnsignedSmallIntegerField(blank=True, null=True)),
                ('edns_max_udp_payload', dnsvizapp.fields.UnsignedSmallIntegerField(blank=True, null=True)),
                ('edns_flags', dnsvizapp.fields.UnsignedIntegerField(blank=True, null=True)),
                ('edns_options', models.BinaryField(blank=True, null=True)),
                ('error', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('errno', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('response_time', models.PositiveSmallIntegerField()),
                ('history_serialized', models.CharField(blank=True, max_length=4096, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')])),
                ('msg_size', dnsvizapp.fields.UnsignedSmallIntegerField(blank=True, null=True)),
                ('query', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='dnsvizapp.dnsquery')),
            ],
        ),
        migrations.CreateModel(
            name='DNSServer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DomainName',
            fields=[
                ('name', dnsvizapp.fields.DomainNameField(max_length=2048, primary_key=True, serialize=False)),
                ('analysis_start', models.DateTimeField(blank=True, null=True)),
                ('refresh_interval', models.PositiveIntegerField(blank=True, null=True)),
                ('refresh_offset', models.PositiveIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='NSMapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', dnsvizapp.fields.DomainNameField(max_length=2048)),
                ('server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dnsvizapp.dnsserver')),
            ],
            options={
                'unique_together': {('name', 'server')},
            },
        ),
        migrations.CreateModel(
            name='NSNameNegativeResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', dnsvizapp.fields.DomainNameField(max_length=2048, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ResourceRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', dnsvizapp.fields.DomainNameField(max_length=2048)),
                ('rdtype', dnsvizapp.fields.UnsignedSmallIntegerField()),
                ('rdclass', dnsvizapp.fields.UnsignedSmallIntegerField()),
                ('rdata_wire', models.BinaryField()),
                ('rdata_name', dnsvizapp.fields.DomainNameField(blank=True, db_index=True, max_length=2048, null=True)),
                ('rdata_address', models.GenericIPAddressField(blank=True, db_index=True, null=True)),
            ],
            options={
                'unique_together': {('name', 'rdtype', 'rdclass', 'rdata_wire')},
            },
        ),
        migrations.CreateModel(
            name='ResourceRecordDNSKEYRelated',
            fields=[
                ('resourcerecord_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dnsvizapp.resourcerecord')),
                ('algorithm', models.PositiveSmallIntegerField()),
                ('key_tag', dnsvizapp.fields.UnsignedSmallIntegerField(db_index=True)),
                ('expiration', models.DateTimeField(blank=True, null=True)),
                ('inception', models.DateTimeField(blank=True, null=True)),
            ],
            bases=('dnsvizapp.resourcerecord',),
        ),
        migrations.CreateModel(
            name='OnlineDomainNameAnalysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', dnsvizapp.fields.DomainNameField(max_length=2048)),
                ('stub', models.BooleanField(default=False)),
                ('analysis_type', dnsvizapp.fields.UnsignedSmallIntegerField(default=0)),
                ('explicit_delegation', models.BooleanField(default=False)),
                ('follow_ns', models.BooleanField(default=False)),
                ('follow_mx', models.BooleanField(default=False)),
                ('analysis_start', models.DateTimeField()),
                ('analysis_end', models.DateTimeField(db_index=True)),
                ('dep_analysis_end', models.DateTimeField()),
                ('version', models.PositiveSmallIntegerField(default=26)),
                ('parent_name_db', dnsvizapp.fields.DomainNameField(blank=True, max_length=2048, null=True)),
                ('dlv_parent_name_db', dnsvizapp.fields.DomainNameField(blank=True, max_length=2048, null=True)),
                ('nxdomain_ancestor_name_db', dnsvizapp.fields.DomainNameField(blank=True, max_length=2048, null=True)),
                ('referral_rdtype', dnsvizapp.fields.UnsignedSmallIntegerField(blank=True, null=True)),
                ('auth_rdtype', dnsvizapp.fields.UnsignedSmallIntegerField(blank=True, null=True)),
                ('cookie_rdtype', dnsvizapp.fields.UnsignedSmallIntegerField(blank=True, null=True)),
                ('nxdomain_name', dnsvizapp.fields.DomainNameField(blank=True, max_length=2048, null=True)),
                ('nxdomain_rdtype', dnsvizapp.fields.UnsignedSmallIntegerField(blank=True, null=True)),
                ('nxrrset_name', dnsvizapp.fields.DomainNameField(blank=True, max_length=2048, null=True)),
                ('nxrrset_rdtype', dnsvizapp.fields.UnsignedSmallIntegerField(blank=True, null=True)),
                ('auth_ns_ip_mapping_db', models.ManyToManyField(related_name='_dnsvizapp_onlinedomainnameanalysis_auth_ns_ip_mapping_db_+', to='dnsvizapp.NSMapping')),
                ('auth_ns_negative_response_db', models.ManyToManyField(related_name='_dnsvizapp_onlinedomainnameanalysis_auth_ns_negative_response_db_+', to='dnsvizapp.NSNameNegativeResponse')),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dnsvizapp.onlinedomainnameanalysis')),
            ],
            options={
                'get_latest_by': 'analysis_end',
                'unique_together': {('name', 'group'), ('name', 'analysis_end')},
            },
            bases=(dnsviz.analysis.offline.OfflineDomainNameAnalysis, models.Model),
        ),
        migrations.CreateModel(
            name='DNSQueryOptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flags', dnsvizapp.fields.UnsignedSmallIntegerField()),
                ('edns_max_udp_payload', dnsvizapp.fields.UnsignedSmallIntegerField(blank=True, null=True)),
                ('edns_flags', dnsvizapp.fields.UnsignedIntegerField(blank=True, null=True)),
                ('edns_options', models.BinaryField(blank=True, null=True)),
                ('tcp_first', models.BooleanField(default=False)),
            ],
            options={
                'unique_together': {('flags', 'edns_max_udp_payload', 'edns_flags', 'edns_options', 'tcp_first')},
            },
        ),
        migrations.AddField(
            model_name='dnsquery',
            name='analysis',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='queries_db', to='dnsvizapp.onlinedomainnameanalysis'),
        ),
        migrations.AddField(
            model_name='dnsquery',
            name='options',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='queries', to='dnsvizapp.dnsqueryoptions'),
        ),
        migrations.CreateModel(
            name='OfflineDomainNameAnalysis',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('dnsvizapp.onlinedomainnameanalysis',),
        ),
        migrations.CreateModel(
            name='ResourceRecordWithAddressInRdata',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('dnsvizapp.resourcerecord',),
        ),
        migrations.CreateModel(
            name='ResourceRecordWithNameInRdata',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('dnsvizapp.resourcerecord',),
        ),
        migrations.CreateModel(
            name='ResourceRecordMapper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.PositiveSmallIntegerField()),
                ('order', models.PositiveSmallIntegerField()),
                ('raw_name', dnsvizapp.fields.DomainNameField(blank=True, max_length=2048, null=True)),
                ('ttl', dnsvizapp.fields.UnsignedIntegerField()),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rr_mappings', to='dnsvizapp.dnsresponse')),
                ('rdata', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dnsvizapp.resourcerecord')),
            ],
            options={
                'unique_together': {('message', 'rdata', 'section')},
            },
        ),
        migrations.CreateModel(
            name='ResourceRecordA',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('dnsvizapp.resourcerecordwithaddressinrdata',),
        ),
        migrations.CreateModel(
            name='ResourceRecordDNSKEY',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('dnsvizapp.resourcerecorddnskeyrelated',),
        ),
        migrations.CreateModel(
            name='ResourceRecordDS',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('dnsvizapp.resourcerecorddnskeyrelated',),
        ),
        migrations.CreateModel(
            name='ResourceRecordMX',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('dnsvizapp.resourcerecordwithnameinrdata',),
        ),
        migrations.CreateModel(
            name='ResourceRecordNS',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('dnsvizapp.resourcerecordwithnameinrdata',),
        ),
        migrations.CreateModel(
            name='ResourceRecordRRSIG',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('dnsvizapp.resourcerecorddnskeyrelated',),
        ),
        migrations.CreateModel(
            name='ResourceRecordSOA',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('dnsvizapp.resourcerecordwithnameinrdata',),
        ),
    ]