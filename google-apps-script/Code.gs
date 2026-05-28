// ========== PASTE THIS ENTIRE FILE (replace all default code) ==========
// Sheet tab name — change if your tab is not "Sheet1" (check bottom tab in Google Sheets)
var SHEET_NAME = 'Sheet1';

/** Run this once from the editor (select testSetup → Run) to authorize the script */
function testSetup() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(SHEET_NAME) || ss.getSheets()[0];
  Logger.log('OK — sheet: ' + sheet.getName());
}

/** Browser test: open your /exec URL — must return JSON, not "function not found" */
function doGet(e) {
  return jsonResponse_({ status: 'ok', message: 'Booking endpoint ready. POST JSON to save a row.' });
}

/** Called when newbot.html submits a booking or cancellation via server.py */
function doPost(e) {
  try {
    var data = {};
    if (e && e.postData && e.postData.contents) {
      data = JSON.parse(e.postData.contents);
    }
    
    if (data.action === 'cancel') {
      var ok = cancelBookingRow_(data.bookingId);
      if (ok) {
        return jsonResponse_({ status: 'success', ok: true, message: 'Booking ' + data.bookingId + ' cancelled successfully.' });
      } else {
        return jsonResponse_({ status: 'error', ok: false, error: 'Booking ID not found.' });
      }
    }
    
    appendBookingRow_(data);
    return jsonResponse_({ status: 'success', ok: true });
  } catch (err) {
    return jsonResponse_({ status: 'error', ok: false, error: String(err) });
  }
}

function cancelBookingRow_(bookingId) {
  if (!bookingId) return false;
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(SHEET_NAME) || ss.getSheets()[0];
  var dataRange = sheet.getDataRange();
  var values = dataRange.getValues();
  var headers = values[0];
  var map = buildHeaderMap_(headers);
  var bookingIdCol = map['booking id'];
  var statusCol = map['booking status'];
  
  if (bookingIdCol === undefined || statusCol === undefined) return false;
  
  for (var i = 1; i < values.length; i++) {
    if (String(values[i][bookingIdCol]).trim() === String(bookingId).trim()) {
      sheet.getRange(i + 1, statusCol + 1).setValue("Cancelled");
      return true;
    }
  }
  return false;
}


function appendBookingRow_(data) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(SHEET_NAME) || ss.getSheets()[0];
  var headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  var map = buildHeaderMap_(headers);
  var ts = new Date();
  var names = splitName_(data.name || '');

  var row = new Array(headers.length);
  for (var i = 0; i < row.length; i++) row[i] = '';

  setCell_(row, map, 'Booking ID', data.bookingId || ('FFS-' + Date.now()));
  setCell_(row, map, 'Timestamp', ts);
  setCell_(row, map, 'First Name', names.first);
  setCell_(row, map, 'Last Name', names.last);
  setCell_(row, map, 'Phone Number', data.mobile || '');
  setCell_(row, map, 'Email Adrress', data.email || '');
  setCell_(row, map, 'Email Address', data.email || '');
  setCell_(row, map, 'Room Type', data.room || '');
  setCell_(row, map, 'Room Rate', data.roomRate != null ? data.roomRate : '');
  setCell_(row, map, 'Adults', data.adults != null ? data.adults : '');
  setCell_(row, map, 'Children', data.children != null ? data.children : '');
  setCell_(row, map, 'Children Age Group', data.childAgeGroup || '');
  setCell_(row, map, 'Check in', data.checkin || '');
  setCell_(row, map, 'Check Out', data.checkout || '');
  setCell_(row, map, 'Nights', data.nights != null ? data.nights : '');
  setCell_(row, map, 'Add- ons', data.addons || '');
  setCell_(row, map, 'Add-ons', data.addons || '');
  setCell_(row, map, 'Add- ons Amount', data.addonsAmount != null ? data.addonsAmount : '');
  setCell_(row, map, 'Add-ons Amount', data.addonsAmount != null ? data.addonsAmount : '');
  setCell_(row, map, 'Coupon Code', data.couponCode || '');
  setCell_(row, map, 'Discount', data.roomDiscount != null ? data.roomDiscount : '');
  setCell_(row, map, 'Total', data.totalAmount != null ? data.totalAmount : '');
  setCell_(row, map, 'Payment Method', data.paymentMethod || '');
  setCell_(row, map, 'Payment Status', formatPaymentStatus_(data));
  setCell_(row, map, 'Booking Status', bookingStatus_(data));
  setCell_(row, map, 'Whatsapp Sent', data.paymentMethod === 'whatsapp' ? 'Yes' : 'Pending');
  setCell_(row, map, 'Special Requests', data.specialRequests || '');
  setCell_(row, map, 'Pay Now', data.payNow != null ? data.payNow : '');
  setCell_(row, map, 'Room Amount', data.roomAmount != null ? data.roomAmount : '');
  setCell_(row, map, 'Razorpay Payment ID', data.razorpay_payment_id || '');

  sheet.appendRow(row);
}

function buildHeaderMap_(headers) {
  var map = {};
  for (var i = 0; i < headers.length; i++) {
    var key = String(headers[i] || '').trim().toLowerCase();
    if (key) map[key] = i;
  }
  return map;
}

function setCell_(row, map, header, value) {
  var idx = map[String(header).trim().toLowerCase()];
  if (idx !== undefined) row[idx] = value;
}

function splitName_(full) {
  full = String(full).trim();
  if (!full) return { first: '', last: '' };
  var parts = full.split(/\s+/);
  if (parts.length === 1) return { first: parts[0], last: '' };
  return { first: parts[0], last: parts.slice(1).join(' ') };
}

function formatPaymentStatus_(data) {
  var s = data.paymentStatus || 'PENDING';
  if (data.razorpay_payment_id) s += ' | ' + data.razorpay_payment_id;
  if (data.qrScreenshotBase64) s += ' | QR screenshot attached';
  return s;
}

function bookingStatus_(data) {
  if (data.paymentStatus === 'PAID') return 'Confirmed (paid)';
  if (data.paymentStatus === 'SCREENSHOT_UPLOADED') return 'Awaiting verification';
  if (data.paymentStatus === 'WHATSAPP_BOOKING') return 'WhatsApp inquiry';
  if (data.paymentStatus === 'UPI_LINK_OPENED') return 'UPI pending';
  return 'New';
}

function jsonResponse_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
