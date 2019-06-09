from enum import Enum


class Codigos(Enum):
	"""Clase con los nombres y primeros bits en hexadecimal que identifican los protocolos conocidos mas utilizados en las TXs OP_RETURN"""

	# CATEGORIA
	# PROTOCOLO = CODIGO_HEX

	# ARTE DIGITAL
	ASCRIBE = "4153435249424";
	BLOCKAI = "1f00";
	MONEGRAPH = "4d47";

	# BIENES
	COINSPARK = "53504b";
	COLU = "4343";
	COUNTERPARTY = "434e5452505254";
	OMNI = "6f6d6e69";
	OPENASSETS = "4f41";

	# DOCUMENTOS NOTARIALES
	BITPROOF = "42495450524f4f";
	BLOCKSIGN = "4253";
	CRYPTOCOPYRIGHT = "43727970746f50726f6f66";
	FACTOM = "4661", "4641";
	LAPREUVE = "4c615072657576";
	NICOSIA = "554e696344432";
	ORIGINALMY = "4f5249474d";
	PROOFOFEXISTENCE = "444f4350524f4f";
	PROVEBIT = "50726f76654269";
	REMEMBR = "524d42";
	STAMPD = "5354414d504423";
	STAMPERY = "5331","5332","5333", "5334","5335", "5336","5337", "5338", "5339";
	TRADLE = "747261646c";

	# OTROS
	BLOCKSTORE = "6964", "5888", "5808";
	ETERNITYWALL = "455720";
	SMARTBIT = "53422e";
	
	# PROTOCOLO IDENTIFICADO PERO DESCONOCIDA PROCEDENCIA
	LP_UNKNOWN = "4c50"