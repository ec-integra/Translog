import struct
import os
import csv
from datetime import datetime

# Инициализируем таблицы и глобальные переменные
myPI = 3.141592653589793
consumption = ''
DJIFrameList = []
DJIFrameList.extend(['start',
                     'OSD',
                     'Home',
                     'Gimbal',
                     'RemoteController',
                     'CUSTOM',
                     'DEFORM',
                     'Battery',
                     'SmartBattery',
                     'Message',
                     'WARNING',
                     'RemoteController-GPS',
                     'RemoteController-DEBUG',
                     'RECOVER',
                     'APPGPS',
                     'FIRMWARE',
                     'OFDM',
                     'VISION',
                     'VISION-WARNING',
                     'MC',
                     'APP-operation',
                     '??',
                     '??',
                     '??',
                     'APPSER',
                     '??',
                     '??'])
DJIFrameList.extend(['??' for x in range(0, 228)])
DJIFrameList[40] = 'Component'
DJIFrameList[57] = 'JPG'

DJIFrame = {'OSD': [],
            'Home': [],
            'Gimbal': [],
            'RemoteController': [],
            'CUSTOM': [],
            'DEFORM': [],
            'Battery': [],
            'SmartBattery': [],
            'Message': [],
            'WARNING': [],
            'RemoteController-GPS': [],
            'RemoteController-DEBUG': [],
            'RECOVER': [],
            'APPGPS': [],
            'FIRMWARE': [],
            'OFDM': [],
            'VISION': [],
            'VISION-WARNING': [],
            'MC': [],
            'APP-operation': [],
            'COMPONENT': [],
            'JPG': [],
            'APPSER': [],
            'unknown': [],
            'Detail': [],
            'Optional': []}

crc64Table = [0x0, 0x7AD870C830358979, 0xF5B0E190606B12F2, 0x8F689158505E9B8B, 0xC038E5739841B68F, 0xBAE095BBA8743FF6,
              0x358804E3F82AA47D, 0x4F50742BC81F2D04, 0xAB28ECB46814FE75, 0xD1F09C7C5821770C, 0x5E980D24087FEC87,
              0x24407DEC384A65FE, 0x6B1009C7F05548FA, 0x11C8790FC060C183, 0x9EA0E857903E5A08, 0xE478989FA00BD371,
              0x7D08FF3B88BE6F81, 0x7D08FF3B88BE6F8, 0x88B81EABE8D57D73, 0xF2606E63D8E0F40A, 0xBD301A4810FFD90E,
              0xC7E86A8020CA5077, 0x4880FBD87094CBFC, 0x32588B1040A14285, 0xD620138FE0AA91F4, 0xACF86347D09F188D,
              0x2390F21F80C18306, 0x594882D7B0F40A7F, 0x1618F6FC78EB277B, 0x6CC0863448DEAE02, 0xE3A8176C18803589,
              0x997067A428B5BCF0, 0xFA11FE77117CDF02, 0x80C98EBF2149567B, 0xFA11FE77117CDF0, 0x75796F2F41224489,
              0x3A291B04893D698D, 0x40F16BCCB908E0F4, 0xCF99FA94E9567B7F, 0xB5418A5CD963F206, 0x513912C379682177,
              0x2BE1620B495DA80E, 0xA489F35319033385, 0xDE51839B2936BAFC, 0x9101F7B0E12997F8, 0xEBD98778D11C1E81,
              0x64B116208142850A, 0x1E6966E8B1770C73, 0x8719014C99C2B083, 0xFDC17184A9F739FA, 0x72A9E0DCF9A9A271,
              0x8719014C99C2B08, 0x4721E43F0183060C, 0x3DF994F731B68F75, 0xB29105AF61E814FE, 0xC849756751DD9D87,
              0x2C31EDF8F1D64EF6, 0x56E99D30C1E3C78F, 0xD9810C6891BD5C04, 0xA3597CA0A188D57D, 0xEC09088B6997F879,
              0x96D1784359A27100, 0x19B9E91B09FCEA8B, 0x636199D339C963F2, 0xDF7ADABD7A6E2D6F, 0xA5A2AA754A5BA416,
              0x2ACA3B2D1A053F9D, 0x50124BE52A30B6E4, 0x1F423FCEE22F9BE0, 0x659A4F06D21A1299, 0xEAF2DE5E82448912,
              0x902AAE96B271006B, 0x74523609127AD31A, 0xE8A46C1224F5A63, 0x81E2D7997211C1E8, 0xFB3AA75142244891,
              0xB46AD37A8A3B6595, 0xCEB2A3B2BA0EECEC, 0x41DA32EAEA507767, 0x3B024222DA65FE1E, 0xA2722586F2D042EE,
              0xD8AA554EC2E5CB97, 0x57C2C41692BB501C, 0x2D1AB4DEA28ED965, 0x624AC0F56A91F461, 0x1892B03D5AA47D18,
              0x97FA21650AFAE693, 0xED2251AD3ACF6FEA, 0x95AC9329AC4BC9B, 0x7382B9FAAAF135E2, 0xFCEA28A2FAAFAE69,
              0x8632586ACA9A2710, 0xC9622C4102850A14, 0xB3BA5C8932B0836D, 0x3CD2CDD162EE18E6, 0x460ABD1952DB919F,
              0x256B24CA6B12F26D, 0x5FB354025B277B14, 0xD0DBC55A0B79E09F, 0xAA03B5923B4C69E6, 0xE553C1B9F35344E2,
              0x9F8BB171C366CD9B, 0x10E3202993385610, 0x6A3B50E1A30DDF69, 0x8E43C87E03060C18, 0xF49BB8B633338561,
              0x7BF329EE636D1EEA, 0x12B592653589793, 0x4E7B2D0D9B47BA97, 0x34A35DC5AB7233EE, 0xBBCBCC9DFB2CA865,
              0xC113BC55CB19211C, 0x5863DBF1E3AC9DEC, 0x22BBAB39D3991495, 0xADD33A6183C78F1E, 0xD70B4AA9B3F20667,
              0x985B3E827BED2B63, 0xE2834E4A4BD8A21A, 0x6DEBDF121B863991, 0x1733AFDA2BB3B0E8, 0xF34B37458BB86399,
              0x8993478DBB8DEAE0, 0x6FBD6D5EBD3716B, 0x7C23A61DDBE6F812, 0x3373D23613F9D516, 0x49ABA2FE23CC5C6F,
              0xC6C333A67392C7E4, 0xBC1B436E43A74E9D, 0x95AC9329AC4BC9B5, 0xEF74E3E19C7E40CC, 0x601C72B9CC20DB47,
              0x1AC40271FC15523E, 0x5594765A340A7F3A, 0x2F4C0692043FF643, 0xA02497CA54616DC8, 0xDAFCE7026454E4B1,
              0x3E847F9DC45F37C0, 0x445C0F55F46ABEB9, 0xCB349E0DA4342532, 0xB1ECEEC59401AC4B, 0xFEBC9AEE5C1E814F,
              0x8464EA266C2B0836, 0xB0C7B7E3C7593BD, 0x71D40BB60C401AC4, 0xE8A46C1224F5A634, 0x927C1CDA14C02F4D,
              0x1D148D82449EB4C6, 0x67CCFD4A74AB3DBF, 0x289C8961BCB410BB, 0x5244F9A98C8199C2, 0xDD2C68F1DCDF0249,
              0xA7F41839ECEA8B30, 0x438C80A64CE15841, 0x3954F06E7CD4D138, 0xB63C61362C8A4AB3, 0xCCE411FE1CBFC3CA,
              0x83B465D5D4A0EECE, 0xF96C151DE49567B7, 0x76048445B4CBFC3C, 0xCDCF48D84FE7545, 0x6FBD6D5EBD3716B7,
              0x15651D968D029FCE, 0x9A0D8CCEDD5C0445, 0xE0D5FC06ED698D3C, 0xAF85882D2576A038, 0xD55DF8E515432941,
              0x5A3569BD451DB2CA, 0x20ED197575283BB3, 0xC49581EAD523E8C2, 0xBE4DF122E51661BB, 0x3125607AB548FA30,
              0x4BFD10B2857D7349, 0x4AD64994D625E4D, 0x7E7514517D57D734, 0xF11D85092D094CBF, 0x8BC5F5C11D3CC5C6,
              0x12B5926535897936, 0x686DE2AD05BCF04F, 0xE70573F555E26BC4, 0x9DDD033D65D7E2BD, 0xD28D7716ADC8CFB9,
              0xA85507DE9DFD46C0, 0x273D9686CDA3DD4B, 0x5DE5E64EFD965432, 0xB99D7ED15D9D8743, 0xC3450E196DA80E3A,
              0x4C2D9F413DF695B1, 0x36F5EF890DC31CC8, 0x79A59BA2C5DC31CC, 0x37DEB6AF5E9B8B5, 0x8C157A32A5B7233E,
              0xF6CD0AFA9582AA47, 0x4AD64994D625E4DA, 0x300E395CE6106DA3, 0xBF66A804B64EF628, 0xC5BED8CC867B7F51,
              0x8AEEACE74E645255, 0xF036DC2F7E51DB2C, 0x7F5E4D772E0F40A7, 0x5863DBF1E3AC9DE, 0xE1FEA520BE311AAF,
              0x9B26D5E88E0493D6, 0x144E44B0DE5A085D, 0x6E963478EE6F8124, 0x21C640532670AC20, 0x5B1E309B16452559,
              0xD476A1C3461BBED2, 0xAEAED10B762E37AB, 0x37DEB6AF5E9B8B5B, 0x4D06C6676EAE0222, 0xC26E573F3EF099A9,
              0xB8B627F70EC510D0, 0xF7E653DCC6DA3DD4, 0x8D3E2314F6EFB4AD, 0x256B24CA6B12F26, 0x788EC2849684A65F,
              0x9CF65A1B368F752E, 0xE62E2AD306BAFC57, 0x6946BB8B56E467DC, 0x139ECB4366D1EEA5, 0x5CCEBF68AECEC3A1,
              0x2616CFA09EFB4AD8, 0xA97E5EF8CEA5D153, 0xD3A62E30FE90582A, 0xB0C7B7E3C7593BD8, 0xCA1FC72BF76CB2A1,
              0x45775673A732292A, 0x3FAF26BB9707A053, 0x70FF52905F188D57, 0xA2722586F2D042E, 0x854FB3003F739FA5,
              0xFF97C3C80F4616DC, 0x1BEF5B57AF4DC5AD, 0x61372B9F9F784CD4, 0xEE5FBAC7CF26D75F, 0x9487CA0FFF135E26,
              0xDBD7BE24370C7322, 0xA10FCEEC0739FA5B, 0x2E675FB4576761D0, 0x54BF2F7C6752E8A9, 0xCDCF48D84FE75459,
              0xB71738107FD2DD20, 0x387FA9482F8C46AB, 0x42A7D9801FB9CFD2, 0xDF7ADABD7A6E2D6, 0x772FDD63E7936BAF,
              0xF8474C3BB7CDF024, 0x829F3CF387F8795D, 0x66E7A46C27F3AA2C, 0x1C3FD4A417C62355, 0x935745FC4798B8DE,
              0xE98F353477AD31A7, 0xA6DF411FBFB21CA3, 0xDC0731D78F8795DA, 0x536FA08FDFD90E51, 0x29B7D047EFEC8728]


def write2csv(output, input, deli, full, id):
    """
    Запись csv файла таблиц
    :param output: выходной путь
    :param input: входной файл
    :param deli: разделитель
    :param full: режим обработки
    :param id: номер файла
    :return:
    """
    name, ext = os.path.splitext(os.path.basename(input))
    if not os.path.exists(output):
        os.makedirs(output)

    if (full):
        maxlen = 0
        for item in DJIFrame:
            if len(DJIFrame[item]) > maxlen:
                maxlen = len(DJIFrame[item])

        headers = []
        with open(os.path.join(output, name + "_FULL" + ' (' + str(id) + ')' + ".csv"), 'w') as csvfile:
            w = csv.writer(csvfile, delimiter=deli, lineterminator="\n")

            lenframes = {}
            for item in DJIFrame:
                if len(DJIFrame[item]) > 0 and item != 'Optional':
                    itemen = len(DJIFrame[item][0])
                    lenframes[item] = itemen
                    for title in DJIFrame[item][0]:
                        headers.append(item + '.' + title)
            w.writerow(headers)

            i = 1
            while i < maxlen:
                data = []
                for item in DJIFrame:
                    if len(DJIFrame[item]) > i and item != 'Optional':
                        for title in DJIFrame[item][i]:
                            data.append(title)
                    elif len(DJIFrame[item]) > 0 and item != 'Optional':
                        for q in range(lenframes[item]):
                            data.append("")
                i += 1
                w.writerow(data)

            csvfile.close()
    else:
        if len(DJIFrame['Optional']) > 0:
            with open(os.path.join(output, name + "_OPT" + ' (' + str(id) + ')' + ".csv"), 'w') as csvfile:
                w = csv.writer(csvfile, delimiter=deli, lineterminator="\n")
                for row in DJIFrame['Optional']:
                    if row[0] != '' and row[1] != '':
                        w.writerow(row)
                csvfile.close()


#    for item in DJIFrame:
#        if len(DJIFrame[item]) > 0:
#            with open(os.path.join(dir, item + ".csv"), 'w') as csvfile:
#                w = csv.writer(csvfile, delimiter=deli, lineterminator="\n")
#                for row in DJIFrame[item]:
#                    w.writerow(row)
#                csvfile.close()

def unscramble(payload, record_type):
    result = []
    if len(payload) < 1:
        raise Exception("BAD Payload! Payload format error ", payload)
    key = payload[0]
    crc = (key + record_type) & 0xff
    dataforBUFFER = 0x123456789ABCDEF0 * key

    bufferToCRC = [0 for x in range(0, 8)]
    for i in range(8):
        bufferToCRC[i] = dataforBUFFER & 0xff
        dataforBUFFER >>= 8

    for i in range(8):
        tableIndex = (bufferToCRC[i] ^ crc) & 0xff
        crc = crc64Table[tableIndex] ^ (crc >> 8)
    scrambleBytes = [0 for x in range(0, 8)]
    for i in range(8):
        scrambleBytes[i] = crc & 0xff
        crc >>= 8
    for index in range(1, len(payload)):
        result.append(payload[index] ^ scrambleBytes[(index - 1) % 8])
    return result


def OSD(payload):
    motorFailReason, ctrlDevice = 0, 0
    if len(payload) > 53:
        longitude, \
        latitude, \
        height, \
        xSpeed, \
        ySpeed, \
        zSpeed, \
        pitch, \
        roll, \
        yaw, \
        byte1, \
        flycCommandRAW, \
        byte2, \
        byte3, \
        byte4, \
        byte5, \
        gpsNum, \
        flightActionRAW, \
        motorStartFailedCause, \
        byte6, \
        battery, \
        sWaveHeight, \
        flyTime, \
        motorRevolution, \
        unkonwn2Bytes, \
        flycVersion, \
        droneType, \
        imuInitFailReason, \
        motorFailReason, \
        unkonwn1byte, \
        ctrlDevice = struct.unpack_from('<ddhhhhhhhBBBBBBBBBBBBHBHBBBBBB', payload, 0)
    else:
        longitude, \
        latitude, \
        height, \
        xSpeed, \
        ySpeed, \
        zSpeed, \
        pitch, \
        roll, \
        yaw, \
        byte1, \
        flycCommandRAW, \
        byte2, \
        byte3, \
        byte4, \
        byte5, \
        gpsNum, \
        flightActionRAW, \
        motorStartFailedCause, \
        byte6, \
        battery, \
        sWaveHeight, \
        flyTime, \
        motorRevolution, \
        unkonwn2Bytes, \
        flycVersion, \
        droneType, \
        imuInitFailReason = struct.unpack_from('<ddhhhhhhhBBBBBBBBBBBBHBHBBB', payload, 0)
    if len(DJIFrame['OSD']) == 0:
        # add Header
        DJIFrame['OSD'].append(
            ['PayloadSize', "longitude", "latitude", "height", "xSpeed", "ySpeed", "zSpeed", "pitch", "roll", "yaw",
             "rcState", "flycState",
             "flycCommandRAW",
             "goHomeStatus", "isSwaveWork", "isMotorUp", "groundOrSky", "canIOCWork",
             "modeChannel", "isImuPreheated", "voltageWarning", "isVisionUsed",
             "batteryType", "gpsLevel", "waveError", "compassError",
             "isAcceletorOverRange", "isVibrating", "isBarometerDeadInAir", "isNotEnoughForce", "isMotorBlocked",
             "isPropellerCatapult", "isGoHomeHeightModified", "isOutOfLimit",
             "gpsNum", "flightActionRAW", "motorStartFailedCause",
             "waypointLimitMode", "nonGPSCause",
             "battery",
             "sWaveHeight",
             "flyTime",
             "motorRevolution",
             "unkonwn2Bytes",
             "flycVersion", "droneType", "imuInitFailReason",
             "motorFailReason", "ctrlDevice"])
    flongitude = str(longitude * 180 / myPI)
    flongitude = flongitude.replace('.', '')

    flatitude = str(latitude * 180 / myPI)
    flatitude = flatitude.replace('.', '')
    DJIFrame['OSD'].append(
        [len(payload), flongitude, flatitude, height * 0.1, xSpeed * 0.1, ySpeed * 0.1,
         zSpeed * 0.1, pitch * 0.1, roll * 0.1, yaw * 0.1,
         (byte1 & 0x80) >> 7, byte1 & 0x7f,
         flycCommandRAW,
         (byte2 & 0xe0) >> 5, (byte2 & 0x10) >> 4, (byte2 & 0x08) >> 3, (byte2 & 0x06) >> 1, byte2 & 0x01,
         (byte3 & 0x60) >> 5, (byte3 & 0x10) >> 4, (byte3 & 0x06) >> 1, byte3 & 0x01,
         (byte4 & 0xc0) >> 6, (byte4 & 0x3c) >> 2, (byte4 & 0x02) >> 1, byte4 & 0x01,
         (byte5 & 0x80) >> 7, (byte5 & 0x40) >> 6, (byte5 & 0x20) >> 5, (byte5 & 0x10) >> 4, (byte5 & 0x08) >> 3,
         (byte5 & 0x04) >> 2, (byte5 & 0x02) >> 1, byte5 & 0x01,
         gpsNum, flightActionRAW, motorStartFailedCause,
         (byte6 & 0x10) >> 4, byte6 & 0x0f,
         battery, sWaveHeight * 0.1, flyTime * 0.1, motorRevolution, unkonwn2Bytes, flycVersion, droneType,
         imuInitFailReason, motorFailReason, ctrlDevice])

    if len(DJIFrame['Optional']) > 0:
        if DJIFrame['Optional'][-1][1] == "" or DJIFrame['Optional'][-1][0] == "":
            DJIFrame['Optional'][-1][1] = flyTime * 0.1
            DJIFrame['Optional'][-1][4] = flongitude
            DJIFrame['Optional'][-1][5] = flatitude
            DJIFrame['Optional'][-1][6] = height * 0.1
            DJIFrame['Optional'][-1][7] = xSpeed * 0.1
            DJIFrame['Optional'][-1][8] = ySpeed * 0.1
            DJIFrame['Optional'][-1][9] = zSpeed * 0.1
            DJIFrame['Optional'][-1][10] = pitch * 0.1
            DJIFrame['Optional'][-1][11] = roll * 0.1
            DJIFrame['Optional'][-1][12] = yaw * 0.1
            DJIFrame['Optional'][-1][13] = (byte4 & 0x3c) >> 2
            DJIFrame['Optional'][-1][14] = gpsNum

            DJIFrame['Optional'][-1][17] = consumption
        else:
            DJIFrame['Optional'].append(
                ['', flyTime * 0.1, "", "", flongitude, flatitude, height * 0.1, xSpeed * 0.1,
                 ySpeed * 0.1,
                 zSpeed * 0.1, pitch * 0.1, roll * 0.1, yaw * 0.1, (byte4 & 0x3c) >> 2, gpsNum, "", "", consumption])

    else:
        DJIFrame['Optional'].append(
            ['datetime', "flytime", "hSpeed", "distance", "longitude", "latitude", "height", "xSpeed", "ySpeed",
             "zSpeed", "pitch", "roll", "yaw", "gpsLevel", "gpsNum", "noise", "jamming", "consumption"])
        DJIFrame['Optional'].append(
            ['', flyTime * 0.1, "", "", flongitude, flatitude, height * 0.1, xSpeed * 0.1, ySpeed * 0.1,
             zSpeed * 0.1, pitch * 0.1, roll * 0.1, yaw * 0.1, (byte4 & 0x3c) >> 2, gpsNum, "", "", consumption])


def Home(payload):
    longitude, \
    latitude, \
    height, \
    byte1, \
    byte2, \
    goHomeHeight, \
    courseLockAngle, \
    dataRecorderStatus, \
    dataRecorderRemainCapacity, \
    dataRecorderRemainTime, \
    dataRecorderFileIndex, \
    ss, \
    maxAllowedHeight, \
    restStr, \
    unknown = struct.unpack_from('<ddfBBHHBBHH5sf' + str(len(payload) - 50) + 's9s', payload, 0)
    if len(DJIFrame['Home']) == 0:
        # add Header
        DJIFrame['Home'].append(['PayloadSize', "longitude", "latitude", "height",
                                 "hasGoHome", "goHomeStatus", "isDynamicHomePointEnabled", "aircraftHeadDirection",
                                 "goHomeMode", "isHomeRecord",
                                 "iocMode", "isIOCEnabled", "isBeginnerMode", "isCompassCeleing", "compassCeleStatus",
                                 "goHomeHeight", "courseLockAngle", "dataRecorderStatus", "dataRecorderRemainCapacity",
                                 "dataRecorderRemainTime", "dataRecorderFileIndex",
                                 "maxAllowedHeight", "unkonwnString", "unknownbyte"])
    flongitude = str(longitude * 180 / myPI)
    flongitude = flongitude.replace('.', '')

    flatitude = str(latitude * 180 / myPI)
    flatitude = flatitude.replace('.', '')
    DJIFrame['Home'].append([len(payload), flongitude, flatitude, height * 0.1,
                             (byte1 & 0x80) >> 7, (byte1 & 0x70) >> 4, (byte1 & 0x08) >> 3, (byte1 & 0x04) >> 2,
                             (byte1 & 0x02) >> 1, byte1 & 0x01,
                             (byte2 & 0xe0) >> 5, (byte2 & 0x10) >> 4, (byte2 & 0x08) >> 3, (byte2 & 0x04) >> 2,
                             byte2 & 0x03,
                             goHomeHeight, courseLockAngle * 0.1, dataRecorderStatus, dataRecorderRemainCapacity,
                             dataRecorderRemainTime, dataRecorderFileIndex, maxAllowedHeight,
                             restStr.decode('utf-8', errors='ignore'), [x for x in unknown]])


def Gimbal(payload):
    pitch, \
    roll, \
    yaw, \
    GIMBALmode, \
    rollAdjust, \
    yawAngle, \
    byte1, \
    byte2 = struct.unpack_from('<hhhBbhBB', payload, 0)
    if len(DJIFrame['Gimbal']) == 0:
        # add Header
        DJIFrame['Gimbal'].append(['PayloadSize', "pitch", "roll", "yaw",
                                   "GIMBALmode", "rollAdjust", "yawAngle",
                                   "isStuck", "autoCalibrationResult", "isAutoCalibration", "isYawInLimit",
                                   "isRollInLimit", "isPitchInLimit",
                                   "isSingleClick", "isTripleClick", "isDoubleClick", "version"])
    DJIFrame['Gimbal'].append([len(payload), pitch * 0.1, roll * 0.1, yaw * 0.1,
                               (GIMBALmode & 0xc0) >> 6, rollAdjust * 0.1, yawAngle * 0.1,
                               (byte1 & 0x40) >> 6, (byte1 & 0x10) >> 4, (byte1 & 0x08) >> 3, (byte1 & 0x04) >> 2,
                               (byte1 & 0x02) >> 1, byte1 & 0x01,
                               (byte2 & 0x80) >> 7, (byte2 & 0x40) >> 6, (byte2 & 0x20) >> 5, byte2 & 0x0f])


def RemoteController(payload):
    aileron, \
    elevator, \
    throttle, \
    rudder, \
    gimbal, \
    wheelOffset, \
    byte1, \
    byte2 = struct.unpack_from('<hhhhhBBB', payload, 0)
    if len(DJIFrame['RemoteController']) == 0:
        # add Header
        DJIFrame['RemoteController'].append(['PayloadSize', "aileron", "elevator", "throttle",
                                             "rudder", "gimbal", "wheelOffset",
                                             "RCmode", "goHome",
                                             "record", "shutter", "playback", "custom1", "custom2"])
    DJIFrame['RemoteController'].append(
        [len(payload), (aileron - 1024) / 0.066, (elevator - 1024) / 0.066, (throttle - 1024) / 0.066,
         (rudder - 1024) / 0.066, (gimbal - 1024) / 0.066,
         (wheelOffset & 0x3e) >> 1,
         (byte1 & 0x30) >> 4, (byte1 & 0x08) >> 3,
         (byte2 & 0x80) >> 7, (byte2 & 0x40) >> 6, (byte2 & 0x20) >> 5, (byte2 & 0x10) >> 4, (byte2 & 0x08) >> 3])


def CUSTOM(payload):
    unkonwn2Bytes, \
    hSpeed, \
    distance, \
    updateTime = struct.unpack_from('<HffQ', payload, 0)
    if len(DJIFrame['CUSTOM']) == 0:
        # add Header
        DJIFrame['CUSTOM'].append(['PayloadSize', "hSpeed", "distance", "updateTime"])
    # DJIFrame['CUSTOM'].append([len(payload), hSpeed, distance, updateTime])
    DJIFrame['CUSTOM'].append(
        [len(payload), hSpeed, distance, datetime.utcfromtimestamp(updateTime / 1000).strftime('%Y-%m-%d %H:%M:%S:%f')])

    if len(DJIFrame['Optional']) > 0:
        if DJIFrame['Optional'][-1][1] == "" or DJIFrame['Optional'][-1][0] == "":
            DJIFrame['Optional'][-1][0] = updateTime
            DJIFrame['Optional'][-1][2] = hSpeed
            DJIFrame['Optional'][-1][3] = distance
            DJIFrame['Optional'][-1][17] = consumption
        else:
            DJIFrame['Optional'].append(
                [updateTime, "", hSpeed, distance, "", "", "", "", "", "", "", "", "", "", "", "", "", consumption])

    else:
        DJIFrame['Optional'].append(
            ['datetime', "flytime", "hSpeed", "distance", "longitude", "latitude", "height", "xSpeed", "ySpeed",
             "zSpeed", "pitch", "roll", "yaw", "gpsLevel", "gpsNum", "noise", "jamming", "consumption"])
        DJIFrame['Optional'].append(
            [updateTime, "", hSpeed, distance, "", "", "", "", "", "", "", "", "", "", "", "", "", consumption])


def DEFORM(payload):
    byte1 = struct.unpack_from('<B', payload, 0)
    if len(DJIFrame['DEFORM']) == 0:
        # add Header
        DJIFrame['DEFORM'].append(['PayloadSize', "deformMode", "deformStatus", "isDeformProtected"])
    DJIFrame['CUSTOM'].append([len(payload), (byte1 & 0x30) >> 4, (byte1 & 0x0e) >> 1, byte1 & 0x01])


# ??????NOT in USE????
def Battery(payload):
    relativeCapacity, \
    currentPV, \
    currentCapacity, \
    fullCapacity, \
    life, \
    loopNum, \
    errorType, \
    current, \
    voltageCell1, \
    voltageCell2, \
    voltageCell3, \
    voltageCell4, \
    voltageCell15, \
    voltageCell6, \
    serialNo, \
    productDate, \
    temperature, \
    connStatus = struct.unpack_from('<BHHHBHLHHHHHHHHHHB', payload, 0)
    if len(DJIFrame['Battery']) == 0:
        # add Header
        DJIFrame['Battery'].append(['PayloadSize', "relativeCapacity", "currentPV", "currentCapacity",
                                    "fullCapacity", "life", "loopNum",
                                    "errorType", "current",
                                    "voltageCell1", "voltageCell2", "voltageCell3", "voltageCell4", "voltageCell5",
                                    "voltageCell6",
                                    "serialNo", "productDate", "temperature", "connStatus"])
    DJIFrame['Battery'].append(
        [len(payload), relativeCapacity, currentPV / 1000, currentCapacity, fullCapacity, life, loopNum,
         errorType, current / 1000, voltageCell1 / 1000, voltageCell2 / 1000, voltageCell3 / 1000, voltageCell4 / 1000,
         voltageCell5 / 1000,
         voltageCell6 / 1000, serialNo, productDate, temperature / 100, connStatus])


def SmartBattery(payload):
    usefulTime, \
    goHomeTime, \
    landTime, \
    goHomeBattery, \
    landBattery, \
    safeFlyRadius, \
    volumeConsume, \
    status, \
    goHomeStatus, \
    goHomeCountdown, \
    voltage, \
    battery, \
    byte1, \
    byte2, \
    voltagePercent = struct.unpack_from('<HHHHHLfLBBHBBBB', payload, 0)
    global consumption
    consumption = volumeConsume
    if len(DJIFrame['SmartBattery']) == 0:
        # add Header
        DJIFrame['SmartBattery'].append(['PayloadSize', "usefulTime", "goHomeTime", "landTime",
                                         "goHomeBattery", "landBattery", "safeFlyRadius",
                                         "volumeConsume", "status",
                                         "goHomeStatus", "goHomeCountdown", "voltage", "battery", "lowWarningGoHome",
                                         "lowWarning",
                                         "seriousLowWarningLanding", "seriousLowWarning", "voltagePercent"])

    DJIFrame['SmartBattery'].append(
        [len(payload), usefulTime, goHomeTime, landTime, goHomeBattery, landBattery, safeFlyRadius, volumeConsume,
         status,
         goHomeStatus, goHomeCountdown, voltage / 1000,
         (byte1 & 0x80) >> 7, byte1 & 0x7f,
         (byte2 & 0x80) >> 7, byte2 & 0x7f,
         voltagePercent])


def Message(payload):
    if len(DJIFrame['Message']) == 0:
        # add Header
        DJIFrame['Message'].append(['PayloadSize', "MESSAGE"])
    DJIFrame['Message'].append([len(payload), payload.decode('utf-8', errors='ignore')])


# print(DJIFrame['Message'])

def WARNING(payload):
    if len(DJIFrame['WARNING']) == 0:
        # add Header
        DJIFrame['WARNING'].append(['PayloadSize', "WARNING"])
    DJIFrame['WARNING'].append([len(payload), payload.decode('utf-8', errors='ignore')])


# print(DJIFrame['WARNING'])

def RECOVER(payload):
    if len(payload) < 109:
        raise Exception("RECOVER Length too small!")
    droneType, \
    appType, \
    appVersionL, \
    appVersionM, \
    appVersionH, \
    aircraftSn, \
    aircraftName, \
    activeTimestamp, \
    cameraSn, \
    rcSn, \
    batterySn = struct.unpack_from('<BBBBB16s32sL16s16s16s', payload, 0)
    if len(DJIFrame['RECOVER']) == 0:
        DJIFrame['RECOVER'].append(
            ['PayloadSize', 'droneType', 'appType', 'appVersion', 'aircraftSn', 'aircraftName', 'activeTimestamp',
             'cameraSn', 'rcSn', 'batterySn'])
    DJIFrame['RECOVER'].append(
        [len(payload), droneType, appType, (appVersionH << 16) | (appVersionM << 8) | appVersionL,
         aircraftSn.decode('utf-8', errors='ignore'), aircraftName.decode('utf-8', errors='ignore'),
         datetime.utcfromtimestamp(activeTimestamp).strftime('%Y-%m-%d %H:%M:%S'),
         cameraSn.decode('utf-8', errors='ignore'), rcSn.decode('utf-8', errors='ignore'),
         batterySn.decode('utf-8', errors='ignore')])


def APPGPS(payload):
    latitude, \
    longitude, \
    accuracy = struct.unpack_from('<ddf', payload, 0)
    flongitude = str(longitude)
    flongitude = flongitude.replace('.', '')

    flatitude = str(latitude)
    flatitude = flatitude.replace('.', '')
    if len(DJIFrame['APPGPS']) == 0:
        DJIFrame['APPGPS'].append(['PayloadSize', 'latitude', 'longitude', 'accuracy'])
    DJIFrame['APPGPS'].append([len(payload), flatitude, flongitude, accuracy])


def FIRMWARE(payload):
    unknown, \
    versionL, \
    versionM, \
    versionH, \
    Firmstr = struct.unpack_from('<HBBB' + str(len(payload) - 5) + 's', payload, 0)
    if len(DJIFrame['FIRMWARE']) == 0:
        DJIFrame['FIRMWARE'].append(['PayloadSize', 'version', 'unkonwn'])
    DJIFrame['FIRMWARE'].append([len(payload), (versionH << 18) | (versionM << 8) | versionL, [c for c in Firmstr]])


def APPSER(payload):
    if len(DJIFrame['APPSER']) == 0:
        # add Header
        DJIFrame['APPSER'].append(['PayloadSize', "WARNING"])
    DJIFrame['APPSER'].append([len(payload), payload.decode('utf-8', errors='ignore')])


# print(DJIFrame['WARNING'])

def COMPONENT(payload):
    select = ['', '', '', '', '']
    componentType, \
    serialNumberLength = struct.unpack_from('<HB', payload, 0)
    string = struct.unpack_from('<' + str(serialNumberLength) + 's', payload, 3)
    select[componentType - 1] = string[0].decode('utf-8', errors='ignore')
    if len(DJIFrame['COMPONENT']) == 0:
        DJIFrame['COMPONENT'].append(
            ['PayloadSize', 'componentType', 'serialNumberLength', 'cameraSn', 'aircraftSn', 'rcSn', 'batterySn',
             'unknownSn'])
    DJIFrame['COMPONENT'].append(
        [len(payload), componentType, serialNumberLength, select[0], select[1], select[2], select[3], select[4]])


def JPG(payload):
    lastByte = 0
    resultPic = []
    picIndex = 0
    for x in payload:
        if ((lastByte << 8) | x) == 0xFFD8:
            resultPic.append([255, 216])
        if ((lastByte << 8) | x) == 0xFFD9:
            resultPic[picIndex].append(255)
            resultPic[picIndex].append(217)
            picIndex = picIndex + 1
        if x == 0xff:
            return 0
        if len(resultPic) > 0:
            resultPic[picIndex].append(x)
        lastByte = x
    if len(resultPic) == 0:
        return 0

    header = ["PayloadSize"]
    inside = [len(payload)]
    for i in range(len(resultPic)):
        header.append("Pic_" + str(len(i + 1)))
        inside.append(resultPic[i])
    if len(DJIFrame['JPG']) == 0:
        DJIFrame['JPG'].append(header)
    DJIFrame['JPG'].append(inside)


def parserDetail(payload, version):
    print('Dealing with detail! start here')

    #  DETAILS.cityPart: string (length 20):
    #  DETAILS.street: string (length 20):
    #  DETAILS.city: string (length 20):
    #  DETAILS.area: string (length 20):
    #  DETAILS.isFavorite: 1 byte unsigned:
    #  DETAILS.isNew: 1 byte unsigned:
    #  DETAILS.needsUpload: 1 byte unsigned:
    #  DETAILS.recordLineCount: 4 bytes little-endian unsigned:
    #  unknown (4 bytes):
    #  DETAILS.timestamp: 8 bytes little-endian, multiple of 0.001 seconds, in Unix time format:
    #  DETAILS.longitude: 8 bytes little-endian double, in degrees:
    #  DETAILS.latitude: 8 bytes little-endian double, in degrees:
    #  DETAILS.totalDistance: 4 bytes little-endian float:
    #  DETAILS.totalTime: 4 bytes little-endian unsigned:
    #  DETAILS.maxHeight: 4 bytes little-endian float:
    #  DETAILS.maxHorizontalSpeed: 4 bytes little-endian float:
    #  DETAILS.maxVerticalSpeed: 4 bytes little-endian float:
    #  DETAILS.photoNum: 4 bytes little-endian unsigned:
    #  DETAILS.videoTime: 4 bytes little-endian unsigned:
    #  here total : 143 bytes
    activeTimestamp = 0

    cityPart, \
    street, \
    city, \
    area, \
    isFavorite, \
    isNew, \
    needUpload, \
    recordLineCount, \
    unknown4bytes, \
    timestamp, \
    longitude, \
    latitude, \
    totalDistance, \
    totalTime, \
    maxHeight, \
    maxHorizontalSpeed, \
    maxVerticalSpeed, \
    photoNum, \
    videoTime = struct.unpack_from("<20s20s20s20sBBBLLQddfLfffLL", payload, 0)

    if version < 6:
        unknown124byte, \
        aircraftSn, \
        unknown1byte, \
        aircraftName, \
        unknown7bytes, \
        activeTimestamp, \
        cameraSn, \
        rcSn, \
        batterySn, \
        appType, \
        appVersion = struct.unpack_from("<124s10sB25s7sQ10s10s10sB3s", payload, 143)
    else:
        unknown137byte, \
        aircraftName, \
        aircraftSn, \
        cameraSn, \
        rcSn, \
        batterySn, \
        appType, \
        appVersion = struct.unpack_from("<137s32s16s16s16s16sB3s", payload, 143)
        appversion2 = 0
    if len(DJIFrame['Detail']) == 0:
        DJIFrame['Detail'].append(
            ['cityPart', 'street', 'city', 'area', 'isFavorite', 'isNew', 'needUpload', 'recordLineCount',
             'timestamp', 'longitude', 'latitude', 'totalDistance', 'totalTime', 'maxHeight', 'maxHorizontalSpeed',
             'maxVerticalSpeed',
             'photoNum', 'videoTime', 'aircraftName', 'aircraftSn', 'cameraSn', 'rcSn', 'batterySn',
             'appType', 'appVersion', 'activeTimestamp'])
        flongitude = str(longitude)
        flongitude = flongitude.replace('.', '')

        flatitude = str(latitude)
        flatitude = flatitude.replace('.', '')
        DJIFrame['Detail'].append([cityPart.decode('utf-8', errors='ignore'), street.decode('utf-8', errors='ignore'),
                                   city.decode('utf-8', errors='ignore'), area.decode('utf-8', errors='ignore'),
                                   isFavorite, isNew, needUpload, recordLineCount,
                                   datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S'),
                                   flongitude,
                                   flatitude, totalDistance, totalTime / 1000, maxHeight, maxHorizontalSpeed,
                                   maxVerticalSpeed,
                                   photoNum, videoTime, aircraftName.decode('utf-8', errors='ignore'),
                                   aircraftSn.decode('utf-8', errors='ignore'),
                                   cameraSn.decode('utf-8', errors='ignore'), rcSn.decode('utf-8', errors='ignore'),
                                   batterySn.decode('utf-8', errors='ignore'),
                                   appType, '.'.join([str(x) for x in appVersion]),
                                   datetime.utcfromtimestamp(activeTimestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')])


def UNKNOWN(payload, type):
    if len(DJIFrame['unknown']) == 0:
        DJIFrame['unknown'].append(['type', 'length', 'payload'])
    DJIFrame['unknown'].append([type, len(payload), [x for x in payload]])


def parserBody(body, version, detail, recordEnd):
    headsize = 0
    isScrambled = 0
    recordStart = 0
    detailStart = 0
    detailEnd = 0
    computeFileSize = 0

    if version < 6:
        headsize = 12
    else:
        headsize = 100
        isScrambled = 1

    if version >= 12:
        recordStart = headsize + detail
        detailStart = headsize
        detailEnd = detailStart + detail
        computeFileSize = recordEnd
    else:
        recordStart = headsize
        detailStart = recordEnd
        detailEnd = detailStart + detail
        computeFileSize = detailEnd

    if computeFileSize < headsize + 3:
        raise Exception("BAD FILE! file format error ", computeFileSize)

    recordArea = body[recordStart:recordEnd + 1]

    i = 0
    frameNumber = 1
    while i < len(recordArea):
        record_type = recordArea[i]
        # JPG format
        if record_type == 57:
            JPG(recordArea[i + 2:])
            break
        else:
            record_size = recordArea[i + 1]
            payload = recordArea[i + 2:i + 2 + record_size]
            record_end = recordArea[i + 2 + record_size]
            if record_end != 255:
                raise Exception("File not right")
                break
            i += record_size + 3
            #print("Dealing with frame", frameNumber, " with type: ", DJIFrameList[record_type])
            frameNumber = frameNumber + 1
            # unscramble payload!
            if isScrambled > 0:
                payload = bytearray(unscramble(payload, record_type))
            # pass
            #print(payload)
            if record_type == 1:
                OSD(payload)
            elif record_type == 5:
                CUSTOM(payload)
            elif record_type == 4:
                RemoteController(payload)
            elif record_type == 3:
                Gimbal(payload)
            elif record_type == 2:
                Home(payload)
            elif record_type == 6:
                DEFORM(payload)
            elif record_type == 7:
                Battery(payload)
            elif record_type == 8:
                SmartBattery(payload)
            elif record_type == 9:
                Message(payload)
            elif record_type == 10:
                WARNING(payload)
            # elif record_type == 11:
            # 	GPSFrame(payload)
            # elif record_type == 12:
            # 	DebugFrame(payload)
            elif record_type == 13:
                RECOVER(payload)
            elif record_type == 14:
                APPGPS(payload)
            elif record_type == 15:
                FIRMWARE(payload)
            elif record_type == 24:
                APPSER(payload)
            elif record_type == 40:
                COMPONENT(payload)
            else:
                UNKNOWN(payload, record_type)

    parserDetail(body[detailStart:detailEnd], version)


# Character	Byte order	Size	Alignment
# @(默认)	本机	本机	本机,凑够4字节
# =	本机	标准	none,按原字节数
# <	小端	标准	none,按原字节数
# >	大端	标准	none,按原字节数
# !	network(大端)	标准	none,按原字节数


# 格式符		C语言类型		Python类型		Standard size
# x			pad byte		no value
# c			char			string of length 1	1
# b			signed char		integer				1
# B			unsigned char	integer				1
# ?			_Bool			bool				1
# h			short			integer				2
# H			unsigned 		short	integer		2
# i			int				integer				4
# I(大写的i)	unsigned int	integer				4
# l(小写的L)	long			integer				4
# L			unsigned long	long				4
# q			long long		long				8
# Q			unsigned long 	long				8
# f			float			float				4
# d			double			float				8
# s			char[]			string
# p			char[]			string
# P			void *			long

def decode_file(path):
    with open(path, 'rb') as f:
        body = f.read()
        __header, \
        __detailAreaBytes, \
        __version = struct.unpack_from('<Qhb', body, 0)
        # print(hex(__header),__detailAreaBytes,hex(__version))
        parserBody(body, __version, __detailAreaBytes, __header)


def txttocsv(input, output, deli, full, id):
    """
    Перевод TXT логов и запись в csv файл
    :param input: входной файл
    :param output: выходной путь
    :param deli: разделитель в таблицах
    :param full: режим обработки
    :param id: номер файла для записи
    :return:
    """
    global DJIFrameList
    global DJIFrame

    # Переинициализируем таблицы
    DJIFrameList = []
    DJIFrameList.extend(['start',
                         'OSD',
                         'Home',
                         'Gimbal',
                         'RemoteController',
                         'CUSTOM',
                         'DEFORM',
                         'Battery',
                         'SmartBattery',
                         'Message',
                         'WARNING',
                         'RemoteController-GPS',
                         'RemoteController-DEBUG',
                         'RECOVER',
                         'APPGPS',
                         'FIRMWARE',
                         'OFDM',
                         'VISION',
                         'VISION-WARNING',
                         'MC',
                         'APP-operation',
                         '??',
                         '??',
                         '??',
                         'APPSER',
                         '??',
                         '??'])
    DJIFrameList.extend(['??' for x in range(0, 228)])
    DJIFrameList[40] = 'Component'
    DJIFrameList[57] = 'JPG'

    DJIFrame = {'OSD': [],
                'Home': [],
                'Gimbal': [],
                'RemoteController': [],
                'CUSTOM': [],
                'DEFORM': [],
                'Battery': [],
                'SmartBattery': [],
                'Message': [],
                'WARNING': [],
                'RemoteController-GPS': [],
                'RemoteController-DEBUG': [],
                'RECOVER': [],
                'APPGPS': [],
                'FIRMWARE': [],
                'OFDM': [],
                'VISION': [],
                'VISION-WARNING': [],
                'MC': [],
                'APP-operation': [],
                'COMPONENT': [],
                'JPG': [],
                'APPSER': [],
                'unknown': [],
                'Detail': [],
                'Optional': []}
    file_path = input
    if os.path.exists(file_path):
        decode_file(file_path)
        # print(DJIFrame)
        write2csv(output, input, deli, full, id)
    else:
        raise Exception('Oops, file name error')
