from typing import Any, Dict, Tuple
from django.db import models

# Create your models here.

from django.db import models

from django.db import models

from django.db import models

class ProxyServerInfo(models.Model):
    """
    Tabel ini berisi informasi tentang server proxy.
    """
    server_name = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    location = models.CharField(max_length=255)
    admin_contact = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.server_name

class UserAgentLog(models.Model):
    """
    Tabel ini berisi informasi log User-Agent dari permintaan HTTP.
    """
    timestamp = models.DateTimeField()
    user_agent = models.CharField(max_length=1024)
    ip_address = models.GenericIPAddressField()
    request_url = models.URLField()
    http_method = models.CharField(max_length=10)
    response_status = models.CharField(max_length=10)
    response_size = models.IntegerField()
    server = models.ForeignKey(ProxyServerInfo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.timestamp} - {self.user_agent}"


class AccessLog(models.Model):
    """
    Tabel ini berisi log akses dari Squid Proxy.
    """
    timestamp = models.CharField(max_length=50)
    elapsed_time = models.IntegerField(help_text="Waktu yang dihabiskan untuk permintaan dalam milidetik")
    client_address = models.GenericIPAddressField()
    http_status = models.CharField(max_length=50)
    bytes = models.IntegerField(help_text="Jumlah byte yang dikirim ke klien")
    request_method = models.CharField(max_length=200)
    request_url = models.URLField()
    host = models.CharField(max_length=255, blank=True, null=True)
    server = models.ForeignKey(ProxyServerInfo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.timestamp} - {self.client_address}"


class CacheLog(models.Model):
    """
    Tabel ini berisi log cache dari Squid Proxy.
    """
    timestamp = models.DateTimeField()
    cache_status = models.CharField(max_length=50, help_text="Status cache seperti HIT, MISS, dll.")
    client_address = models.GenericIPAddressField()
    bytes = models.IntegerField(help_text="Jumlah byte yang di-cache")
    request_method = models.CharField(max_length=10)
    request_url = models.URLField()
    mime_type = models.CharField(max_length=255)
    server = models.ForeignKey(ProxyServerInfo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.timestamp} - {self.cache_status}"


class StoreLog(models.Model):
    """
    Tabel ini berisi log store dari Squid Proxy yang mencatat penyimpanan dan penghapusan objek di cache.
    """
    timestamp = models.DateTimeField()
    realese = models.CharField(max_length=255)
    flag = models.CharField(max_length=255)
    object_number = models.CharField(max_length=255) 
    hash = models.CharField(max_length=50, help_text="Tindakan seperti RELEASE, SWAPOUT, dll.")
    size = models.IntegerField(help_text="Ukuran objek dalam byte")
    timestamp_expire = models.CharField(max_length=255)
    url = models.URLField()
    last_modified = models.CharField(max_length=255)
    http = models.CharField(max_length=10)
    mime_type = models.CharField(max_length=255)
    methode = models.CharField(max_length=255)
    server = models.ForeignKey(ProxyServerInfo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.timestamp} - {self.action} - {self.request_url}"


class SquidLog(models.Model):
    """
    Tabel ini berisi semua jenis log dari Squid Proxy. 
    """
    timestamp = models.DateTimeField()
    server = models.ForeignKey(ProxyServerInfo, on_delete=models.CASCADE)
    access_log = models.ForeignKey(AccessLog, on_delete=models.CASCADE, null=True, blank=True)
    cache_log = models.ForeignKey(CacheLog, on_delete=models.CASCADE, null=True, blank=True)
    store_log = models.ForeignKey(StoreLog, on_delete=models.CASCADE, null=True, blank=True)
    user_agent_log = models.ForeignKey(UserAgentLog, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.timestamp} - {self.server.server_name}"



