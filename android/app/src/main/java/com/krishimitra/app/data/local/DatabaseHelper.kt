package com.krishimitra.app.data.local

import android.content.Context
import android.database.Cursor
import android.database.sqlite.SQLiteDatabase
import android.database.sqlite.SQLiteOpenHelper
import android.util.Log
import com.krishimitra.app.domain.model.Crop
import com.krishimitra.app.domain.model.Disease
import com.krishimitra.app.domain.model.Loan
import com.krishimitra.app.domain.model.Scheme
import java.io.File
import java.io.FileOutputStream

class DatabaseHelper(private val context: Context) : SQLiteOpenHelper(context, DB_NAME, null, DB_VERSION) {

    companion object {
        const val DB_NAME = "krishi_knowledge.db"
        const val DB_VERSION = 1
        private const val TAG = "DatabaseHelper"

        @Volatile
        private var instance: DatabaseHelper? = null

        fun getInstance(context: Context): DatabaseHelper {
            return instance ?: synchronized(this) {
                instance ?: DatabaseHelper(context.applicationContext).also { instance = it }
            }
        }
    }

    init {
        ensureDatabaseExists()
    }

    private fun ensureDatabaseExists() {
        val dbFile = context.getDatabasePath(DB_NAME)
        if (!dbFile.exists()) {
            dbFile.parentFile?.mkdirs()
            try {
                context.assets.open(DB_NAME).use { input ->
                    FileOutputStream(dbFile).use { output ->
                        input.copyTo(output)
                    }
                }
                Log.i(TAG, "Copied pre-seeded knowledge database from assets successfully.")
            } catch (e: Exception) {
                Log.e(TAG, "Failed to copy database from assets: ${e.message}", e)
            }
        }
    }

    override fun onCreate(db: SQLiteDatabase?) {
        // Database is copied pre-populated from assets
    }

    override fun onUpgrade(db: SQLiteDatabase?, oldVersion: Int, newVersion: Int) {
        // Handled via sync API
    }

    fun getAllCrops(): List<Crop> {
        val list = mutableListOf<Crop>()
        val db = readableDatabase
        var cursor: Cursor? = null
        try {
            cursor = db.rawQuery("SELECT * FROM crops ORDER BY name_en ASC", null)
            while (cursor.moveToNext()) {
                list.add(
                    Crop(
                        id = cursor.getString(cursor.getColumnIndexOrThrow("id")),
                        nameEn = cursor.getString(cursor.getColumnIndexOrThrow("name_en")),
                        nameHi = cursor.getString(cursor.getColumnIndexOrThrow("name_hi")),
                        scientificName = cursor.getString(cursor.getColumnIndexOrThrow("scientific_name")),
                        category = cursor.getString(cursor.getColumnIndexOrThrow("category")),
                        categoryHi = cursor.getString(cursor.getColumnIndexOrThrow("category_hi")),
                        soil = cursor.getString(cursor.getColumnIndexOrThrow("soil")),
                        soilHi = cursor.getString(cursor.getColumnIndexOrThrow("soil_hi")),
                        soilPh = cursor.getString(cursor.getColumnIndexOrThrow("soil_ph")),
                        climate = cursor.getString(cursor.getColumnIndexOrThrow("climate")),
                        climateHi = cursor.getString(cursor.getColumnIndexOrThrow("climate_hi")),
                        temperature = cursor.getString(cursor.getColumnIndexOrThrow("temperature")),
                        sowingSeason = cursor.getString(cursor.getColumnIndexOrThrow("sowing_season")),
                        sowingSeasonHi = cursor.getString(cursor.getColumnIndexOrThrow("sowing_season_hi")),
                        irrigation = cursor.getString(cursor.getColumnIndexOrThrow("irrigation")),
                        irrigationHi = cursor.getString(cursor.getColumnIndexOrThrow("irrigation_hi")),
                        fertilizer = cursor.getString(cursor.getColumnIndexOrThrow("fertilizer")),
                        fertilizerHi = cursor.getString(cursor.getColumnIndexOrThrow("fertilizer_hi")),
                        harvesting = cursor.getString(cursor.getColumnIndexOrThrow("harvesting")),
                        harvestingHi = cursor.getString(cursor.getColumnIndexOrThrow("harvesting_hi")),
                        pests = cursor.getString(cursor.getColumnIndexOrThrow("pests")),
                        pestsHi = cursor.getString(cursor.getColumnIndexOrThrow("pests_hi")),
                        diseases = cursor.getString(cursor.getColumnIndexOrThrow("diseases")),
                        diseasesHi = cursor.getString(cursor.getColumnIndexOrThrow("diseases_hi")),
                        cultivationTips = cursor.getString(cursor.getColumnIndexOrThrow("cultivation_tips")),
                        cultivationTipsHi = cursor.getString(cursor.getColumnIndexOrThrow("cultivation_tips_hi")),
                        source = cursor.getString(cursor.getColumnIndexOrThrow("source")),
                        sourceUrl = cursor.getString(cursor.getColumnIndexOrThrow("source_url"))
                    )
                )
            }
        } catch (e: Exception) {
            Log.e(TAG, "Error fetching crops: ${e.message}")
        } finally {
            cursor?.close()
        }
        return list
    }

    fun getAllDiseases(): List<Disease> {
        val list = mutableListOf<Disease>()
        val db = readableDatabase
        var cursor: Cursor? = null
        try {
            cursor = db.rawQuery("SELECT * FROM diseases ORDER BY crop ASC", null)
            while (cursor.moveToNext()) {
                list.add(
                    Disease(
                        id = cursor.getString(cursor.getColumnIndexOrThrow("id")),
                        crop = cursor.getString(cursor.getColumnIndexOrThrow("crop")),
                        cropHi = cursor.getString(cursor.getColumnIndexOrThrow("crop_hi")),
                        diseaseNameEn = cursor.getString(cursor.getColumnIndexOrThrow("disease_name_en")),
                        diseaseNameHi = cursor.getString(cursor.getColumnIndexOrThrow("disease_name_hi")),
                        pathogen = cursor.getString(cursor.getColumnIndexOrThrow("pathogen")),
                        symptomsEn = cursor.getString(cursor.getColumnIndexOrThrow("symptoms_en")),
                        symptomsHi = cursor.getString(cursor.getColumnIndexOrThrow("symptoms_hi")),
                        causesEn = cursor.getString(cursor.getColumnIndexOrThrow("causes_en")),
                        causesHi = cursor.getString(cursor.getColumnIndexOrThrow("causes_hi")),
                        treatmentOrganicEn = cursor.getString(cursor.getColumnIndexOrThrow("treatment_organic_en")),
                        treatmentOrganicHi = cursor.getString(cursor.getColumnIndexOrThrow("treatment_organic_hi")),
                        treatmentChemicalEn = cursor.getString(cursor.getColumnIndexOrThrow("treatment_chemical_en")),
                        treatmentChemicalHi = cursor.getString(cursor.getColumnIndexOrThrow("treatment_chemical_hi")),
                        preventionEn = cursor.getString(cursor.getColumnIndexOrThrow("prevention_en")),
                        preventionHi = cursor.getString(cursor.getColumnIndexOrThrow("prevention_hi")),
                        confidenceThreshold = cursor.getFloat(cursor.getColumnIndexOrThrow("confidence_threshold"))
                    )
                )
            }
        } catch (e: Exception) {
            Log.e(TAG, "Error fetching diseases: ${e.message}")
        } finally {
            cursor?.close()
        }
        return list
    }

    fun getDiseaseById(diseaseId: String): Disease? {
        val db = readableDatabase
        var cursor: Cursor? = null
        try {
            cursor = db.rawQuery("SELECT * FROM diseases WHERE id = ? LIMIT 1", arrayOf(diseaseId))
            if (cursor.moveToFirst()) {
                return Disease(
                    id = cursor.getString(cursor.getColumnIndexOrThrow("id")),
                    crop = cursor.getString(cursor.getColumnIndexOrThrow("crop")),
                    cropHi = cursor.getString(cursor.getColumnIndexOrThrow("crop_hi")),
                    diseaseNameEn = cursor.getString(cursor.getColumnIndexOrThrow("disease_name_en")),
                    diseaseNameHi = cursor.getString(cursor.getColumnIndexOrThrow("disease_name_hi")),
                    pathogen = cursor.getString(cursor.getColumnIndexOrThrow("pathogen")),
                    symptomsEn = cursor.getString(cursor.getColumnIndexOrThrow("symptoms_en")),
                    symptomsHi = cursor.getString(cursor.getColumnIndexOrThrow("symptoms_hi")),
                    causesEn = cursor.getString(cursor.getColumnIndexOrThrow("causes_en")),
                    causesHi = cursor.getString(cursor.getColumnIndexOrThrow("causes_hi")),
                    treatmentOrganicEn = cursor.getString(cursor.getColumnIndexOrThrow("treatment_organic_en")),
                    treatmentOrganicHi = cursor.getString(cursor.getColumnIndexOrThrow("treatment_organic_hi")),
                    treatmentChemicalEn = cursor.getString(cursor.getColumnIndexOrThrow("treatment_chemical_en")),
                    treatmentChemicalHi = cursor.getString(cursor.getColumnIndexOrThrow("treatment_chemical_hi")),
                    preventionEn = cursor.getString(cursor.getColumnIndexOrThrow("prevention_en")),
                    preventionHi = cursor.getString(cursor.getColumnIndexOrThrow("prevention_hi")),
                    confidenceThreshold = cursor.getFloat(cursor.getColumnIndexOrThrow("confidence_threshold"))
                )
            }
        } catch (e: Exception) {
            Log.e(TAG, "Error fetching disease $diseaseId: ${e.message}")
        } finally {
            cursor?.close()
        }
        return null
    }

    fun getAllSchemes(): List<Scheme> {
        val list = mutableListOf<Scheme>()
        val db = readableDatabase
        var cursor: Cursor? = null
        try {
            cursor = db.rawQuery("SELECT * FROM schemes ORDER BY name_en ASC", null)
            while (cursor.moveToNext()) {
                list.add(
                    Scheme(
                        id = cursor.getString(cursor.getColumnIndexOrThrow("id")),
                        nameEn = cursor.getString(cursor.getColumnIndexOrThrow("name_en")),
                        nameHi = cursor.getString(cursor.getColumnIndexOrThrow("name_hi")),
                        category = cursor.getString(cursor.getColumnIndexOrThrow("category")),
                        categoryHi = cursor.getString(cursor.getColumnIndexOrThrow("category_hi")),
                        ministry = cursor.getString(cursor.getColumnIndexOrThrow("ministry")),
                        benefitsEn = cursor.getString(cursor.getColumnIndexOrThrow("benefits_en")),
                        benefitsHi = cursor.getString(cursor.getColumnIndexOrThrow("benefits_hi")),
                        eligibilityEn = cursor.getString(cursor.getColumnIndexOrThrow("eligibility_en")),
                        eligibilityHi = cursor.getString(cursor.getColumnIndexOrThrow("eligibility_hi")),
                        applicationProcessEn = cursor.getString(cursor.getColumnIndexOrThrow("application_process_en")),
                        applicationProcessHi = cursor.getString(cursor.getColumnIndexOrThrow("application_process_hi")),
                        officialUrl = cursor.getString(cursor.getColumnIndexOrThrow("official_url")),
                        source = cursor.getString(cursor.getColumnIndexOrThrow("source")),
                        lastVerified = cursor.getString(cursor.getColumnIndexOrThrow("last_verified"))
                    )
                )
            }
        } catch (e: Exception) {
            Log.e(TAG, "Error fetching schemes: ${e.message}")
        } finally {
            cursor?.close()
        }
        return list
    }

    fun getAllLoans(): List<Loan> {
        val list = mutableListOf<Loan>()
        val db = readableDatabase
        var cursor: Cursor? = null
        try {
            cursor = db.rawQuery("SELECT * FROM loans ORDER BY bank_name ASC", null)
            while (cursor.moveToNext()) {
                list.add(
                    Loan(
                        id = cursor.getString(cursor.getColumnIndexOrThrow("id")),
                        bankName = cursor.getString(cursor.getColumnIndexOrThrow("bank_name")),
                        bankNameHi = cursor.getString(cursor.getColumnIndexOrThrow("bank_name_hi")),
                        loanType = cursor.getString(cursor.getColumnIndexOrThrow("loan_type")),
                        loanTypeHi = cursor.getString(cursor.getColumnIndexOrThrow("loan_type_hi")),
                        purposeEn = cursor.getString(cursor.getColumnIndexOrThrow("purpose_en")),
                        purposeHi = cursor.getString(cursor.getColumnIndexOrThrow("purpose_hi")),
                        interestRate = cursor.getString(cursor.getColumnIndexOrThrow("interest_rate")),
                        interestRateHi = cursor.getString(cursor.getColumnIndexOrThrow("interest_rate_hi")),
                        maxLimit = cursor.getString(cursor.getColumnIndexOrThrow("max_limit")),
                        maxLimitHi = cursor.getString(cursor.getColumnIndexOrThrow("max_limit_hi")),
                        eligibilityEn = cursor.getString(cursor.getColumnIndexOrThrow("eligibility_en")),
                        eligibilityHi = cursor.getString(cursor.getColumnIndexOrThrow("eligibility_hi")),
                        documentsRequired = cursor.getString(cursor.getColumnIndexOrThrow("documents_required")),
                        documentsRequiredHi = cursor.getString(cursor.getColumnIndexOrThrow("documents_required_hi")),
                        officialUrl = cursor.getString(cursor.getColumnIndexOrThrow("official_url")),
                        source = cursor.getString(cursor.getColumnIndexOrThrow("source")),
                        lastVerified = cursor.getString(cursor.getColumnIndexOrThrow("last_verified"))
                    )
                )
            }
        } catch (e: Exception) {
            Log.e(TAG, "Error fetching loans: ${e.message}")
        } finally {
            cursor?.close()
        }
        return list
    }
}
