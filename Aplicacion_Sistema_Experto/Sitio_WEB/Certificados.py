from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.primitives.serialization import PrivateFormat
from cryptography.hazmat.primitives.serialization import NoEncryption
from cryptography.hazmat.primitives.serialization import PublicFormat
from cryptography.hazmat.primitives.serialization import Encoding
import datetime  # Agrega esta línea para importar datetime

# Generar una clave privada RSA
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# Generar el certificado auto-firmado
builder = x509.CertificateBuilder()
builder = builder.subject_name(x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"California"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"My Company"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"http://hornillapp.agrosavia.co:7000/"),
]))
builder = builder.issuer_name(x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"California"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"My Company"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"http://hornillapp.agrosavia.co:7000/"),
]))
builder = builder.not_valid_before(datetime.datetime.utcnow())
builder = builder.not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
builder = builder.public_key(private_key.public_key())
builder = builder.serial_number(x509.random_serial_number())
builder = builder.add_extension(
    x509.SubjectAlternativeName([x509.DNSName(u"http://hornillapp.agrosavia.co:7000/")]),
    critical=False,
)

certificate = builder.sign(
    private_key=private_key, algorithm=hashes.SHA256(),
)

# Exportar la clave privada y el certificado a archivos
with open("key.pem", "wb") as private_key_file:
    private_key_file.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ))

with open("cert.pem", "wb") as certificate_file:
    certificate_file.write(certificate.public_bytes(serialization.Encoding.PEM))
