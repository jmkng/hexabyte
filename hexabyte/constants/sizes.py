"""Size Related Constants."""

# Generic Sizes
BIT = 1
NIBBLE_BITS = 4 * BIT
BYTE_BITS = 8 * BIT
KB = 128 * BYTE_BITS
MB = 1024 * KB

# 32-bit Sizes
WORD32_SZ = 2
WORD32_BITS = BYTE_BITS * WORD32_SZ  # 2 bytes

DWORD32_SZ = 2 * WORD32_SZ
DWORD32_BITS = BYTE_BITS * DWORD32_SZ  # 4 bytes

QWORD32_SZ = 2 * DWORD32_SZ
QWORD32_BITS = BYTE_BITS * QWORD32_SZ  # 8 bytes

PTR32_BITS = DWORD32_BITS  # 4 bytes

# 64-bit Sizes

WORD64_SZ = 4
WORD64_BITS = BYTE_BITS * WORD64_SZ  # 4 bytes

DWORD64_SZ = 2 * WORD64_SZ
DWORD64_BITS = BYTE_BITS * DWORD64_SZ  # 8 bytes

PTR64_BITS = DWORD64_BITS  # 8 bytes

QWORD64_SZ = 2 * DWORD64_SZ
QWORD64_BITS = BYTE_BITS * QWORD64_SZ  # 16 bytes

# Data Source Constants
DEFAULT_BLOCK_SIZE = 4096
